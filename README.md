will register config (location address ports name container info) in etcd when each container is launched.

images can read from etcd instead of from maestro's environment variables.

example.yaml has an example setup. must have etcd deployed

every instance must have ETCD_HOST_ADDRESS as as environment variable

if already using maestro import maestro_etcd_map instead of maestro.guestutils and can call same convenience functions 

each container must have SERVICE_NAME, CONTAINER_NAME, CONTAINER_HOST, ETCD_HOST_ADDRESS