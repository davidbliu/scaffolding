class Container:
	""" 
	containers should know
		- service they belong to (ie: cassandra, kafka, rails)
		- host ip
		- container port/host port mappings
			- dictionary {'containerport':'hostport', 'containerport':'hostport'}
		- image
		- name
	TODO: finish this
	"""
	def __init__(self, name, hostip, portmappings={}, image=""):
		self.name = name
		self.host_ip = hostip
		self.port_mappings = portmappings
		self.image = image

	def register_with_etcd(self, etcd_client):
		print 'registering with etcd'