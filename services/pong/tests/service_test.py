import os
import unittest
import uuid
from unittest.mock import patch

from src.service import PongService
from tests.mocks import MockConsumerRecord


class TestService(unittest.TestCase):

    @patch("src.service.KafkaProducer", spec=True)
    @patch("src.service.uuid", spec=True)
    def test_pong_writes_message_to_kafka_topic(self, mock_uuid, mock_kafka_producer):
        test_uuid = uuid.uuid1()
        mock_uuid.uuid1.return_value = test_uuid
        mock_kafka_producer_instance = mock_kafka_producer.return_value
        service = PongService()
        service.pong()
        mock_kafka_producer_instance.send.assert_called_once_with("", {'message': 'pong', 'uuid': str(test_uuid)})

    @patch("src.service.KafkaProducer", spec=True)
    def test_handle_message_with_invalid_message(self, mock_kafka_producer):
        test_message = {'invalidMessage': 'pung'}
        mock_kafka_producer_instance = mock_kafka_producer.return_value
        mock_consumer_record = MockConsumerRecord(test_message)
        service = PongService()
        service.handle_message(mock_consumer_record)
        self.assertFalse(mock_kafka_producer_instance.send.called, 'send called but was not expected')

    @patch("src.service.KafkaProducer", spec=True)
    def test_handle_message_sends_message_to_kafka_write_topic(self, mock_kafka_producer):
        test_uuid = uuid.uuid1()
        test_message = {'message': 'ping', 'uuid': str(test_uuid)}
        mock_kafka_producer_instance = mock_kafka_producer.return_value
        mock_consumer_record = MockConsumerRecord(test_message)
        service = PongService()
        service.handle_message(mock_consumer_record)
        mock_kafka_producer_instance.send.assert_called_once()

    @patch("src.service.KafkaProducer", spec=True)
    def test_handle_message_flips_ping_and_pong_in_message(self, mock_kafka_producer):
        test_uuid = uuid.uuid1()
        test_message = {'message': 'pong', 'uuid': str(test_uuid)}
        mock_kafka_producer_instance = mock_kafka_producer.return_value
        mock_consumer_record = MockConsumerRecord(test_message)
        service = PongService()
        service.handle_message(mock_consumer_record)
        mock_kafka_producer_instance.send.assert_called_once_with('',
                                                                  {'message': 'ping', 'uuid': str(test_uuid),
                                                                   'deliveries': 1})

    @patch("src.service.KafkaProducer", spec=True)
    def test_handle_message_increments_delivery_counter_in_payload_if_not_exists(self, mock_kafka_producer):
        test_uuid = uuid.uuid1()
        test_message = {'message': 'ping', 'uuid': str(test_uuid)}
        mock_kafka_producer_instance = mock_kafka_producer.return_value
        mock_consumer_record = MockConsumerRecord(test_message)
        service = PongService()
        service.handle_message(mock_consumer_record)
        mock_kafka_producer_instance.send.assert_called_once_with('',
                                                                  {'message': 'pong', 'uuid': str(test_uuid),
                                                                   'deliveries': 1})

    @patch("src.service.KafkaProducer", spec=True)
    def test_handle_message_increments_delivery_counter_in_payload(self, mock_kafka_producer):
        test_uuid = uuid.uuid1()
        test_message = {'message': 'ping', 'uuid': str(test_uuid), 'deliveries': 1}
        mock_kafka_producer_instance = mock_kafka_producer.return_value
        mock_consumer_record = MockConsumerRecord(test_message)
        service = PongService()
        service.handle_message(mock_consumer_record)
        mock_kafka_producer_instance.send.assert_called_once_with('',
                                                                  {'message': 'pong', 'uuid': str(test_uuid),
                                                                   'deliveries': 2})

    @patch("src.service.KafkaProducer", spec=True)
    def test_handle_message_does_not_send_message_once_max_delivery_count_exceeded(self, mock_kafka_producer):
        os.environ['MESSAGE_LIMIT'] = '499'
        test_uuid = uuid.uuid1()
        test_message = {'message': 'ping', 'uuid': str(test_uuid), 'deliveries': 500}
        mock_kafka_producer_instance = mock_kafka_producer.return_value
        mock_consumer_record = MockConsumerRecord(test_message)
        service = PongService()
        service.handle_message(mock_consumer_record)
        self.assertFalse(mock_kafka_producer_instance.send.called, 'send called but was not expected')


if __name__ == '__main__':
    unittest.main()
