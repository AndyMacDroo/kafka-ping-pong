import unittest
from parameterized import parameterized

from src.kafka_config import KafkaConfig
import os


class TestKafkaConfig(unittest.TestCase):

    @parameterized.expand([
        ["", "", ""],
        ["", "test-read", "test-write"],
        ["test:9092", "test-read", "test-write"],
        ["test:9092, test:9093", "test-read", "test-write"],
    ])
    def test_kafka_config_initialise_config_from_environment_variables(self, hosts_string, read_topic, write_topic):
        expected_host = hosts_string
        expected_read_topic = read_topic
        expected_write_topic = write_topic
        os.environ['KAFKA_BROKER_HOSTS'] = expected_host
        os.environ['KAFKA_READ_TOPIC'] = expected_read_topic
        os.environ['KAFKA_WRITE_TOPIC'] = expected_write_topic
        actual_kafka_config = KafkaConfig()
        self.assertEqual(actual_kafka_config.bootstrap_servers, expected_host.split(","))
        self.assertEqual(actual_kafka_config.kafka_read_topic, expected_read_topic)
        self.assertEqual(actual_kafka_config.kafka_write_topic, expected_write_topic)


if __name__ == '__main__':
    unittest.main()
