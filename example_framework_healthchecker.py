import docker
import etcd
import ast
# import simplejson
"""
check health of every container in etcd
if one is down remove it from etcd
"""

keys = ['/cassandra', '/zookeeper', '/rails', '/kafka', '/david']

"""
if container is running: stop and remove it
if container not running: error
"""
def stop_and_remove_container(container_name, host_address):
	base_url = 'tcp://' + host_address + ':4243'
	dockerclient = docker.Client(base_url=base_url, version='1.10', timeout=30)
	dockerclient.stop(container_name)
	dockerclient.remove_container(container_name)

def is_container_running(container_name, host_address):
	base_url = 'tcp://' + host_address + ':4243'
	dockerclient = docker.Client(base_url=base_url, version='1.10', timeout=10)
	try:
		details = dockerclient.inspect_container(container_name)
		# print details
	except:
		return False
	running = details['State']['Running']
	# print details.keys()#
	# print details['HostConfig']['PortBindings']
	if running:
		return True
	return False

def remove_container(container_name, host_address):
	base_url = 'tcp://' + host_address + ':4243'
	dockerclient = docker.Client(base_url=base_url, version='1.10', timeout=10)
	dockerclient.remove_container(container_name)

"""
checks all containers etcd says is running. remove from etcd if they are not running
"""
def check_all_containers(etcd_host_address, etcd_port = 4001):
	# check all containers etcd says is running. if one is not, remove it from etcd.
	etcd_client = etcd.Client(host = etcd_host_address, port = etcd_port)
	for key in keys:
		try:
			instances_dict = ast.literal_eval(etcd_client.read(key).value)
			for instance in instances_dict.keys():
				name = instances_dict[instance]['instance_name']
				host = instances_dict[instance]['instance_host']
				if not is_container_running(name, host):
					print 'the container is not running'
					# remove container if not removed yet
					try:
						remove_container(name, host)
					except:
						print 'already removed....continuing'
					instances_dict.pop(instance, None)
					etcd_client.write(key, instances_dict)
				else:
					print 'this container is running'
		except:
			print 'invalid key ' + key


"""
stop all containers. keys is a global variable defined at top
"""
def stop_all_containers(etcd_host_address, etcd_port = 4001):
	etcd_client = etcd.Client(host = etcd_host_address, port = etcd_port)
	for key in keys:
		try:
			print 'trying to remove this key '+ key
			instances_dict = ast.literal_eval(etcd_client.read(key).value)
			# print instances_dict
			for instance in instances_dict.keys():
				name = instances_dict[instance]['instance_name']
				host = instances_dict[instance]['instance_host']
				if is_container_running(name, host):
					stop_and_remove_container(name, host)
		except:
			print 'invalid key ' + key

def print_all_running_containers(etcd_host_address, etcd_port = 4001):
	etcd_client = etcd.Client(host = etcd_host_address, port = etcd_port)
	for key in keys:
		print 'these are running for ' + key
		instances_dict = ast.literal_eval(etcd_client.read(key).value)
		for instance in instances_dict.keys():
			print "      "+instances_dict[instance]['instance_name']
			print "      "+instances_dict[instance]['instance_host']
			print "..."

# client.delete('/cassandra')
# client.delete('/kafka')
# client.delete('/zookeeper')
# client.delete('/rails')



# check_all_containers('54.189.223.174')

# see if it can stop specific container
# stop_and_remove_container('testcassandra', '54.203.23.229')

stop_all_containers('54.189.223.174')
check_all_containers('54.189.223.174')
print_all_running_containers('54.189.223.174')


