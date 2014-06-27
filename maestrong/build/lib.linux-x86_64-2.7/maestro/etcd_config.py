import etcd
import ast

def register_with_etcd(container):
	"""
	write topology to etcd
	etcd should know where all cassandra nodes are
	under /servicename there you have a dictionary of the services nodes
	"""
	# print container.env
	# if container.name == 'etcd1':
	# 	return
	if 'ETCD_HOST_ADDRESS' not in container.env.keys():
		return
	etcd_host_address = container.env['ETCD_HOST_ADDRESS']
	client = etcd.Client(host = etcd_host_address, port = 4001)
	# client = etcd.Client()

	service_name = container._service.name
	instance_name = container.name
	instance_host = container._ship._ip
	instance_ports = container.ports

	# e_container = etcd_container.Container(instance_name, instance_host)
	instance_dict = {'service_name': service_name,
					 'instance_name': instance_name,
					 'instance_host': instance_host,
					 'port_mapping': instance_ports}

	etcd_key = "/"+service_name
	try:
		old_dict = client.read(etcd_key).value
	except:
		new_dict = {}
		client.write(etcd_key, new_dict)
	full_instances_dict = client.read(etcd_key).value
	full_instances_dict = ast.literal_eval(full_instances_dict)

	full_instances_dict[instance_name] = instance_dict
	client.write(etcd_key, full_instances_dict)


def unregister_with_etcd(container):
	"""
	container is no longer running. remove from etcd
	TODO: perform some action for containers depending on this one
	"""
	client = etcd.Client()
	instance_name = container.name
	service_name = container._service.name
	etcd_key = "/"+service_name
	try:
		full_instances_dict = client.read(etcd_key).value
		full_instances_dict = ast.literal_eval(full_instances_dict)
		full_instances_dict.pop(instance_name, None)
		client.write(etcd_key, full_instances_dict)
	except:
		print "something went wrong"
	