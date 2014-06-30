# example 'framework' does maestros job but more lightweight
# no config file. centralized config is in etcd
# each container needs these env variables: SERVICE_NAME, CONTAINER_NAME, CONTAINER_HOST, ETCD_HOST_ADDRESS

import docker
import etcd
import ast

def register_with_etcd(service, name, host, port_mapping, etcd_host, etcd_port = 4001):
	# throw an error if cannot connect to client?
	etcd_client = etcd.Client(host = etcd_host, port = etcd_port)
	instance_dict = {'service_name': service,
					 'instance_name': name,
					 'instance_host': host,
					 'port_mapping': port_mapping}

	etcd_key = "/"+service
	try:
		old_dict = etcd_client.read(etcd_key).value
	except:
		new_dict = {}
		etcd_client.write(etcd_key, new_dict)
	full_instances_dict = etcd_client.read(etcd_key).value
	full_instances_dict = ast.literal_eval(full_instances_dict)
	full_instances_dict[name] = instance_dict
	etcd_client.write(etcd_key, full_instances_dict)


def launch_container(service, name, host, image, etcd_host, exposed_ports, external_ports, port_mapping):
	baseurl = 'tcp://'+host+':4243'
	# set environment variables
	env = { 'SERVICE_NAME': service, 
			'CONTAINER_NAME': name, 
			'CONTAINER_HOST_ADDRESS': host, 
			'ETCD_HOST_ADDRESS': etcd_host}
	# TODO merge any other env variables into env dictionary
	register_with_etcd(service, name, host, port_mapping, etcd_host)
	# actually launch the container
	dockerclient = docker.Client(base_url=baseurl, version='1.10', timeout=10)
	dockerclient.create_container(image, command=None, hostname=host, user=None,
                   detach=False, stdin_open=False, tty=False, mem_limit=0,
                   ports=exposed_ports, environment=env, dns=None, volumes=None,
                   volumes_from=None, network_disabled=False, name=name,
                   entrypoint=None, cpu_shares=None, working_dir=None)

	# set port bindings. host ports (external) are values keys are exposed ports
	port_bindings = {}
	for index, exposed_port in enumerate(exposed_ports):
		port_bindings[exposed_port] = external_ports[index]
	# set volumes bindings.
	binds = None
	dockerclient.start(name, binds=binds, port_bindings=port_bindings, lxc_conf=None,
        publish_all_ports=False, links=None, privileged=False,
       )

def launch_kafka_container(service, name, host, image, etcd_host):
	print 'launching KAFKA container'
	exposed_ports = [9092]
	external_ports = [9092]
	port_mapping = {}
	port_mapping['kafka_port'] = {}
	port_mapping['kafka_port']['external'] = ('0.0.0.0', str(external_ports[0])+'/tcp')
	port_mapping['kafka_port']['exposed'] = '9092/tcp' # this depends on the image
	baseurl = 'tcp://'+host+':4243'
	# set environment variables
	env = { 'SERVICE_NAME': service, 
			'CONTAINER_NAME': name, 
			'CONTAINER_HOST_ADDRESS': host, 
			'ETCD_HOST_ADDRESS': etcd_host,
			'ZK_PORT_2181_TCP_ADDR' : '54.184.184.23',
          	'ZK_PORT_2181_TCP_PORT' : 2181,
          	'BROKER_ID': 0,
          	'PORT': 9092,
          	'HOST_IP': '54.185.28.145'
			}
	# TODO merge any other env variables into env dictionary
	register_with_etcd(service, name, host, port_mapping, etcd_host)
	# actually launch the container
	dockerclient = docker.Client(base_url=baseurl, version='1.10', timeout=10)
	dockerclient.create_container(image, command=None, hostname=host, user=None,
                   detach=False, stdin_open=False, tty=False, mem_limit=0,
                   ports=exposed_ports, environment=env, dns=None, volumes=None,
                   volumes_from=None, network_disabled=False, name=name,
                   entrypoint=None, cpu_shares=None, working_dir=None)

	# set port bindings. host ports (external) are values keys are exposed ports
	port_bindings = {}
	for index, exposed_port in enumerate(exposed_ports):
		port_bindings[exposed_port] = external_ports[index]
	# set volumes bindings.
	binds = None
	dockerclient.start(name, binds=binds, port_bindings=port_bindings, lxc_conf=None,
        publish_all_ports=False, links=None, privileged=False,
       )

def launch_zk_container(service, name, host, image, etcd_host):
	print 'launching ZOOKEEPER container'
	exposed_ports = [2181]
	external_ports = [2181]
	port_mapping = {}
	port_mapping['client_port'] = {}
	port_mapping['client_port']['external'] = ('0.0.0.0', str(external_ports[0])+'/tcp')
	port_mapping['client_port']['exposed'] = '2181/tcp' # this depends on the image
	launch_container(service, name, host, image, etcd_host, exposed_ports, external_ports, port_mapping)

def launch_rails_container(service, name, host, image, etcd_host):
	print 'launching RAILS container'
	# assume for now service == 'cassandra'
	exposed_ports = [3000]
	# TODO external_ports = get_external_ports(service, host) <--find available external ports automatically
	# check if ports are open: http://stackoverflow.com/questions/19196105/python-how-to-check-if-a-port-is-open-on-linux
	external_ports = [3000]
	port_mapping = {}
	port_mapping['exposedport'] = {}
	port_mapping['exposedport']['external'] = ('0.0.0.0', str(external_ports[0])+'/tcp')
	port_mapping['exposedport']['exposed'] = '3000/tcp' # this depends on the image
	launch_container(service, name, host, image, etcd_host, exposed_ports, external_ports, port_mapping)

def launch_cassandra_container(service, name, host, image, etcd_host):
	print 'launching CASSANDRA container '+name
	# assume for now service == 'cassandra'
	exposed_ports = [9042, 7000, 9160]
	# TODO external_ports = get_external_ports(service, host) <--find available external ports automatically
	external_ports = [9042, 7000, 9160]
	# external_ports = get_next_available_ports(exposed_ports, host)
	port_mapping = {}
	port_mapping['rpc'] = {}
	port_mapping['rpc']['external'] = ('0.0.0.0', str(external_ports[0])+'/tcp')
	port_mapping['rpc']['exposed'] = '9160/tcp' # this depends on the image
	port_mapping['storage'] = {}
	port_mapping['storage']['external'] = ('0.0.0.0', str(external_ports[1])+'/tcp')
	port_mapping['storage']['exposed'] = '7000/tcp' # this depends on the image
	port_mapping['transport'] = {}
	port_mapping['transport']['external'] = ('0.0.0.0', str(external_ports[2])+'/tcp')
	port_mapping['transport']['exposed'] = '9042/tcp' # this depends on the image
	launch_container(service, name, host, image, etcd_host, exposed_ports, external_ports, port_mapping)
	

"""
check if you can run this service on this host
cpu shares etc. available ports
"""
def is_useable(host, service):
	return True

# ports is a list of exposed ports. will get the next set of avaiable ports on the host machine to be external ports.
# for example if ports is [3000] and 3000 is taken but 3001 available, returns [3001]
def get_next_available_ports(ports, host):
	available_ports = []
	for port in ports:
		while not is_port_available(port, host):
			port += 1
		available_ports.append(port)
	return available_ports
def is_port_available(port, host):
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((host, port))
	if result == 0:
	   return True
	return False

def check_port_taken(host, port):
	import socket
	# s = socket.socket()
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		
		s.bind((host, port))
	except socket.error, e:
		print "address already in use"
		print e
def check_server(address, port):
	# Create a TCP socket
	import socket
	s = socket.socket()
	print "Attempting to connect to %s on port %s" % (address, port)
	try:
		s.connect((address, port))
		return True
	except socket.error, e:
		return False

# test out the functions
# etcd_host_address = '54.189.223.174'
# launch_cassandra_container('david', 'testcassandra', '54.203.23.229', 'davidbliu/autocassandrasshd', etcd_host_address)
# print is_port_available(4001, '54.203.23.229')
# print check_server('54.203.23.229', 4001)
# print check_port_taken('54.203.23.229', 4002)

