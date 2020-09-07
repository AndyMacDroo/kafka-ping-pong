import os


class KafkaConfig:

    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BROKER_HOSTS', '').split(",")
        self.kafka_read_topic = os.getenv('KAFKA_READ_TOPIC', '')
        self.kafka_write_topic = os.getenv('KAFKA_WRITE_TOPIC', '')

    def __str__(self):
        return "bootstrap_servers: {0}, kafka_read_topic: {1}, kafka_write_topic: {2}" \
            .format(self.bootstrap_servers, self.kafka_read_topic, self.kafka_write_topic)
