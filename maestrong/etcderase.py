import etcd
import ast

client = etcd.Client()

client.delete('/cassandra')
client.delete('/kafka')
client.delete('/zookeeper')
client.delete('/rails')