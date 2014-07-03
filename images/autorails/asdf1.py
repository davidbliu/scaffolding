import os
import yaml
import etcd
import ast 
from etcd_register import *
# TODO this only works on with etcd on my vm. fix this

#do some tests 
# import maptest

etcd_host_address = os.environ.get('ETCD_HOST_ADDRESS') 
if etcd_host_address is None:
	etcd_host_address = 'localhost' 

	
print etcd_host_address
print 'that was the addr i ised'
client = etcd.Client(host=etcd_host_address, port=4001)
# register this container with etcd so other containers know about it

# register_with_etcd(client)

"""
set up CASSANDRA environment variables
create config/cequel.yml file with keyspace names, cassandra hosts, and ports
by default all ports 9042
"""
cassandra_dict = client.read('/cassandra').value
cassandra_dict = ast.literal_eval(cassandra_dict)
cassandra_hosts = []
for instance in cassandra_dict.keys():
	cassandra_hosts.append(cassandra_dict[instance]["instance_host"])
cassandra_port = 9042

data = {'development':{'hosts':cassandra_hosts, 'port': cassandra_port, 'keyspace':'testapp_development'},
			'test':{'hosts':cassandra_hosts, 'port': cassandra_port, 'keyspace':'testapp_test'},
			'production':{'hosts':cassandra_hosts, 'port': cassandra_port, 'keyspace':'testapp_production'},}
with open('/opt/dockernotes/config/cequel.yml', 'w') as outfile:
	outfile.write(yaml.dump(data, default_flow_style=False))

outfile.close()


"""
set up KAFKA environment variables
set up config/initializers/kafka.yml with kafka broker hosts
by default all ports are 9092
"""
# TODO fix hardcoded port
kafka_dict = client.read("/kafka").value
kafka_dict = ast.literal_eval(kafka_dict)
kafka_hosts = []
kafka_full = []
for instance in kafka_dict.keys():
	kafka_hosts.append(kafka_dict[instance]["instance_host"])
	kafka_full.append(kafka_dict[instance]["instance_host"] + ":9092")

# set write to config/initializers/kafka.yml
with open('/opt/dockernotes/config/initializers/kafka.yml', 'w') as kafka_out:
	kafka_out.write(yaml.dump([kafka_hosts, kafka_full], default_flow_style=True))
kafka_out.close

print 'here are some more infos'

print kafka_hosts
print kafka_full
print cassandra_hosts

os.system('rake cequel:keyspace:create')
os.system('rake cequel:migrate')
os.system("bundle exec rails s")