
def get_node_list(service, ports = ''):
	if service == 'kafka' and ports == '':
		return ['54.185.28.145']
	if service == 'kafka' and ports !='':
		return ['54.185.28.145:9042']
	if service == 'cassandra':
		return ['54.184.184.23', '54.188.5.77', '54.189.247.174']