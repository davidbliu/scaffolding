from example_framework import *

"""
TESTING FULL DEPLOYMENT
launch 3 cassandra containers on 3 different etcd_host_address
launch rails container
cassandra image: davidbliu/acass. cassandr_waiter waits for three nodes before starting any one
rails image: davidbliu/atest . probably wrong, has maestro dependencies. autorails
	atest will be used for maestro demo. either that or webserver2. autorails_waiter
kafka image: davidbliu/kafka
zookeeper image: davidbliu/zookeeper
"""

host1 = '54.184.184.23'
host2 = '54.189.223.174'
host3 = '54.189.247.174'
host4 = '54.185.28.145'
etcd_host_address = '54.189.223.174'
#
# start 3 cassandra containers
#
launch_cassandra_container('cassandra', 'example_cassandra1', host1, 'davidbliu/cassandra_waiter', etcd_host_address)
launch_cassandra_container('cassandra', 'example_cassandra2', host2, 'davidbliu/cassandra_waiter', etcd_host_address)
launch_cassandra_container('cassandra', 'example_cassandra3', host3, 'davidbliu/cassandra_waiter', etcd_host_address)

#
# start 1 zookeeper container
#
launch_zk_container('zookeeper', 'example_zookeeper', host1, 'davidbliu/actzookeeper', etcd_host_address)

#
# start 1 kafka broker
#
launch_kafka_container('kafka', 'example_kafka_broker', host4, 'davidbliu/actkafka', etcd_host_address)

#
# start three rails containers
#
launch_rails_container('david', 'example_rails', host2, 'davidbliu/autorails_waiter', etcd_host_address)