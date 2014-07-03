from marathon import MarathonClient
import urllib2
import json
import etcd
import ast

etcd_host_address = '54.189.223.174'
 
ports = [7000, 9042, 9160]
port_names = ["storage", "transport", "rpc"]

#
# Registers a container with etcd
#
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


def register():
  marathon_client = MarathonClient("http://localhost:8080")
  task_names = ['cassandra1', 'cassandra2', 'cassandra3']
  for t in task_names:
    task = marathon_client.list_tasks(t)[0]
    service = 'cassandra'
    name = t
    # host = task.host  THIS SHOULD HAVE BEEN RIGHT IDK WHATS UP WITH THIS SHIZ
    host = '50.131.237.47'
    port_mapping = {}
    for index in range(0, len(port_names)):
      port_mapping[port_names[index]] = {}
      port_mapping[port_names[index]]["external"] = ('0.0.0.0', str(task.ports[index])+'/tcp')
      port_mapping[port_names[index]]["exposed"] = str(ports[index]) + '/tcp'
    #
    # for testing purposes, print all args for register_with_etcd
    #
    print service
    print name
    print host
    print port_mapping
    register_with_etcd(service, name, host, port_mapping, etcd_host_address)


register()
