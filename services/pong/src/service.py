import os

from kafka import KafkaProducer
import uuid
import json
from nameko.rpc import rpc
import logging
from src.kafka_config import KafkaConfig
from src.utils import current_milli_time
from prometheus_client import start_http_server, Summary, Counter, Histogram
from nameko_kafka import consume, Semantic

kafka_config = KafkaConfig()
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)-15s - [%(levelname)s] - %(funcName)s - %(message)s', level=logging.INFO)

handle_message_timer = Summary('handle_message_time', 'Time spent processing message')
messages_retrieved_counter = Counter('messages_retrieved_from_topic', 'Number of messages retrieved from topic')
pong_request_counter = Counter('pong_requests', 'Number of pong requests')
message_consumption_time_ms = Histogram('message_consumption_time_ms', 'Per message time to consume')


class PongService:
    name = "pong_service"

    # Start Prometheus Metrics Endpoint
    start_http_server(8000)

    @handle_message_timer.time()
    @consume(kafka_config.kafka_read_topic,
             group_id="pong",
             bootstrap_servers=kafka_config.bootstrap_servers,
             semantic=Semantic.AT_LEAST_ONCE)
    def handle_message(self, body):
        self.__generate_message_processing_statistics(body)
        message_ping_pong_limit = os.getenv('MESSAGE_LIMIT')
        decoded_message = json.loads(body.value.decode("utf-8"))
        logger.info("Handling Message: {0}".format(decoded_message))

        if 'message' not in decoded_message or 'uuid' not in decoded_message:
            return body
        if message_ping_pong_limit is not None and "deliveries" in decoded_message:
            if decoded_message['deliveries'] >= int(message_ping_pong_limit):
                logger.info("Max Deliveries of Message Reached: {0}".format(decoded_message))
                return body

        decoded_message = self.__process_message(decoded_message)
        producer = KafkaProducer(bootstrap_servers=kafka_config.bootstrap_servers,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        logger.info("Producing Message: {0}, Topic: {1}".format(decoded_message, kafka_config.kafka_write_topic))
        producer.send(kafka_config.kafka_write_topic, decoded_message)
        producer.flush()
        return body

    @rpc
    def pong(self):
        pong_request_counter.inc()
        message = {'message': 'pong', 'uuid': str(uuid.uuid1())}
        logger.info("Producing Message: {0}, Topic: {1}".format(message, kafka_config.kafka_write_topic))
        producer = KafkaProducer(bootstrap_servers=kafka_config.bootstrap_servers,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(kafka_config.kafka_write_topic, message)
        producer.flush()
        return message

    @staticmethod
    def __process_message(decoded_message):
        if "deliveries" not in decoded_message:
            decoded_message['deliveries'] = 0
        decoded_message['deliveries'] += 1
        decoded_message['message'] = "ping" if decoded_message['message'] == "pong" else "pong"
        return decoded_message

    @staticmethod
    def __generate_message_processing_statistics(body):
        messages_retrieved_counter.inc()
        event_generated_timestamp = body.timestamp
        processing_time = current_milli_time() - event_generated_timestamp
        message_consumption_time_ms.observe(processing_time)
        logger.info("Time taken to consume message (ms): {0}".format(processing_time))
