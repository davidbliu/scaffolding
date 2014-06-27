import etcd
print etcd
def testfunction():
	with open('etcd_output.txt', 'w') as outfile:
		outfile.write("this is a test")

def register_with_etcd(container):

 	"""
 	write topology to etcd
	etcd should know where all cassandra nodes are
		under /cassandra there are many nodes like cassandra1 etcd
		they are storing ip, ports
	"""

	service_name = container._service.name()
	instance_name = container.name()
	instance_host = container._ship._ship
	instance_ports = container._ports

	with open('/home/david/etcd_output.txt', 'a') as outfile:
		outfile.write(str(service_name))
		outfile.write(str(instance_name))
		outfile.write(str(instance_host))
		outfile.write(str(instance_ports))
		outfile.write("-------------------------")
		outfile.write("\n")