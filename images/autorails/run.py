import os
import yaml

from maestro.guestutils import *
# from maestro_test import *

os.system('printenv')

# set environment variables


# cassandra
# os.environ["CASSANDRA_1_ADDR"] = get_specific_host('cassandra', 'cassandra1')
# os.environ["CASSANDRA_2_ADDR"] = get_specific_host('cassandra', 'cassandra2')
# os.environ["CASSANDRA_3_ADDR"] = get_specific_host('cassandra', 'cassandra3')
# os.environ["CASSANDRA_1_PORT"] = '9042'
# os.environ["CASSANDRA_2_PORT"] = '9042'
# os.environ["CASSANDRA_3_PORT"] = '9042'

"""
set up CASSANDRA environment variables
create config/cequel.yml file with keyspace names, cassandra hosts, and ports
by default all ports 9042
"""
cassandra_hosts = get_node_list('cassandra')
cassandra_port = 9042
data = {'development':{'hosts':cassandra_hosts, 'port': cassandra_port, 'keyspace':'testapp_development'},
			'test':{'hosts':cassandra_hosts, 'port': cassandra_port, 'keyspace':'testapp_test'},
			'production':{'hosts':cassandra_hosts, 'port': cassandra_port, 'keyspace':'testapp_production'},}
with open('config/cequel.yml', 'w') as outfile:
	outfile.write(yaml.dump(data, default_flow_style=False))
outfile.close()


"""
set up KAFKA environment variables
set up config/initializers/kafka.yml with kafka broker hosts
by default all ports are 9042
"""
kafka_hosts = get_node_list('kafka')
kafka_full = get_node_list('kafka', ports=['smtp'])
# set write to config/initializers/kafka.yml
with open('config/initializers/kafka.yml', 'w') as kafka_out:
	kafka_out.write(yaml.dump([kafka_hosts, kafka_full], default_flow_style=True))
kafka_out.close




# os.environ["KAFKA_1_ADDR"] = get_specific_host('kafka', 'kafka1')
# os.environ["KAFKA_1_PORT"] = '9092'


# os.environ["DB_PORT_5432_TCP_ADDR"] = get_specific_host('postgres', 'postgres1')
# port = get_specific_port('postgres', 'postgres1', 'smtp')
# os.environ["DB_PORT_5432_TCP_PORT"] = str(port)

# set up database and start rails server
os.system('rake cequel:keyspace:create')
os.system('rake cequel:migrate')
os.system("bundle exec rails s")