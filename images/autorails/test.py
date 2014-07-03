import yaml


# write cequel configuration
hosts = ['1','2','3', '4']
port = 9042
data = {'development':{'hosts':hosts, 'port': port, 'keyspace':'testapp_development'},
'test':{'hosts':hosts, 'port': port, 'keyspace':'testapp_test'},
'production':{'hosts':hosts, 'port': port, 'keyspace':'testapp_production'},
}
with open('config/cequel.yml', 'w') as outfile:
	outfile.write(yaml.dump(data, default_flow_style=False))