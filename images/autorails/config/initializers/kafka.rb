require 'poseidon'
require 'yaml'

# for use in development
# PRODUCER = Poseidon::Producer.new(["54.185.28.145:9092"], "my_test_producer")
# CONSUMER = Poseidon::PartitionConsumer.new("my_test_consumer", "54.185.28.145", 9092,
#                                             "topic1", 0, :earliest_offset)

# for use in production
# PRODUCER = Poseidon::Producer.new([ENV['KAFKA_1_ADDR']+":"+ENV['KAFKA_1_PORT']], "my_test_producer")
# CONSUMER = Poseidon::PartitionConsumer.new("my_test_consumer", ENV['KAFKA_1_ADDR'], 9092,
#                                             "topic1", 0, :earliest_offset)

# reading config from kafka.yml
data = YAML.load_file('config/initializers/kafka.yml')
broker_hosts = data[0]
brokers = data[1]

PRODUCER = Poseidon::Producer.new(brokers, 'my_test_producer')
CONSUMER = Poseidon::PartitionConsumer.new('my_test_consumer', broker_hosts[0], 9092, 'topic1', 0, :earliest_offset)