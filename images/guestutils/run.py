import os
from guestutils import *
import socket
import time

print 'TESTING MAPPED MAESTRO functions'
while True:
	time.sleep(5)
	try:
		print 'get_environment_name():'
		print get_environment_name()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_service_name():'
		print get_service_name()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_container_name():'
		print get_container_name()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_container_host_address():'
		print get_container_host_address()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_container_internal_address():'
		print get_container_internal_address()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_port(name, default = default_port):'
		print get_port('test', 1234)
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_node_list(service, ports=[], minimum=1):'
		print get_node_list('test')
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'
	try:
		print 'get_specific_host(service, container):'
		print get_specific_host('test', 'test1')
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_specific_port(service, container, port, default'
		print get_specific_port('test', 'test1', 'test', 1234)
		print get_specific_port('test', 'test1', 'test')
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_specific_exposed_port(service, container, port, defaul'
		print get_specific_exposed_port('test', 'test1', 'test', 1234)
		print get_specific_exposed_port('test', 'test1', 'test')
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'
