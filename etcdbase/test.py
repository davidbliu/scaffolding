import container
import etcd
import ast

client = etcd.Client()
c = container.Container('test','hostip')

print 'printing container information'
print c.name
print c.host_ip

print 'now using etcd'
client.write('/test/containername', 'bob')
obj = client.read('/test/containername')
print obj