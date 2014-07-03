import maestro.guestutils as orig
import maestro_etcd_map1 as emap

print 'testing maestro and etcdmap'

print orig.get_environment_name()
print emap.get_environment_name()

print 'print orig.get_service_name()'
print orig.get_service_name()
print emap.get_service_name()

print 'get_container_name()'
print orig.get_container_name()
print emap.get_container_name()

print 'get_container_host_address()'
print orig.get_container_host_address()
print emap.get_container_host_address()

print 'get_container_internal_address()'
print orig.get_container_internal_address()
print emap.get_container_internal_address()

print 'get_port(name, default = )'
print orig.get_port('smtp')
print emap.get_port('smtp')

print 'get_node_list(service, ports=None)'
print orig.get_node_list('cassandra')
print emap.get_node_list('cassandra')
print orig.get_node_list('cassandra', ports = ['rpc'])
print emap.get_node_list('cassandra', ports = ['rpc'])

print 'get_specific_host(service, container)'
print orig.get_specific_host('cassandra', 'cassandra1')
print emap.get_specific_host('cassandra', 'cassandra1')

print 'get_specific_port(service, container, port,'
print orig.get_specific_port('cassandra', 'cassandra1', 'storage')
print emap.get_specific_port('cassandra', 'cassandra1', 'storage')

print 'get_specific_exposed_port'
try:
	print orig.get_specific_exposed_port('cassandra', 'cassandra1', 'storage')
except:
	print 'there wasnt one for cassandra'
print emap.get_specific_exposed_port('cassandra', 'cassandra1', 'storage')

try:
	print orig.get_specific_exposed_port('rails', 'rails1', 'smtp')
except:
	print 'there wasnt one for rails'
print emap.get_specific_exposed_port('rails', 'rails1', 'smtp')