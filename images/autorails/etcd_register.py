import etcd
import ast
import os

def register_with_etcd(client):
	try:
		instance_name = os.environ['CONTAINER_NAME']
		host_ip = os.environ['CONTAINER_HOST_ADDRESS']
		service_name = os.environ['SERVICE_NAME']
	except:
		print 'THERE WAS AN ERROR WITH ENVIRONMENT VARIABLES!!!!!!!!!!!!!'
		instance_name = 'rails1'
		host_ip = 'b'
		service_name = 'rails'
	
	instance_dict = {'service_name': service_name,
						 'instance_name': instance_name,
						 'instance_host': host_ip,
						 'port_mapping': {}}
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