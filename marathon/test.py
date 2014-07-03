from marathon import MarathonClient
# marathon_client = MarathonClient("http://localhost:8080")

marathon_client = MarathonClient("http://localhost:8080")

local_env = {}
local_env['ETCD_HOST_ADDRESS'] = '54.189.223.174'
local_env['SERVICE_NAME'] = 'cassandra'
local_env['CONTAINER_HOST_ADDRESS'] = '50.131.237.47'

#
# launch three cassandra containers
#
def launch_cassandra():
  for index in [1,2,3]:
    name = 'cassandra' + str(index)
    local_env['CONTAINER_NAME'] = name
    marathon_client.create_app(
    	container = {
    			"image" : "docker:///davidbliu/cassandra_marathon6"
    		},
    	id = "cassandra"+str(index),
      	instances = "2",
      	cpus = ".1",
      	mem = "128",
      	uris = [ ],
      	env = local_env, 
        ports = [7000, 9042, 9160]
    )


#
# rails
#
def launch_rails():
  local_env['SERVICE_NAME'] = 'rails'
  name = 'rails1'
  local_env['CONTAINER_NAME'] = name
  marathon_client.create_app(
    container = {
        "image" : "docker:///davidbliu/rails_marathon",
        "options": ["--name", name]
      },
    id = name,
      instances = "1",
      cpus = ".1",
      mem = "128",
      uris = [ ],
      env = local_env, 
      ports = [3000]
  )

def list_tasks_out():
  print 'listing out tasks'
  tasks = marathon_client.list_tasks('cassandra2')
  for task in tasks:
    print task.host
    print task.id
    # print task.container
    print task.started_at
    print task.staged_at
# launch_rails()
launch_cassandra()
# list_tasks_out()

#
# cassandra1_0-1404369727583 (LDH domain name rule?)
#
