import json


class MockConsumerRecord:

    def __init__(self, value):
        self.topic = "test"
        self.partition = 0
        self.value = json.dumps(value).encode()
        self.timestamp = 1599424092199
        self.timestamp_type = 0
