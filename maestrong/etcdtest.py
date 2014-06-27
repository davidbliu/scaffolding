import etcd
import ast

# client = etcd.Client()
client = etcd.Client(host='54.184.184.23', port =4001)

try:
	print client.read('/cassandra').value
except:
	print 'no cassandra'
client.write('/testkey', 'test')
print client.read('/testkey').value
# print client.read('/kafka').value
# print client.read('/zookeeper').value
# print client.read('/rails').value
print 'successful'