import json

from flask import Flask
from nameko.standalone.rpc import ServiceRpcProxy
import os

app = Flask(__name__)


def service_rpc_proxy(service):
    config = {'AMQP_URI': os.getenv('AMQP_URI')}
    return ServiceRpcProxy(service, config)


@app.route('/')
def root():
    return "Hello World!"


@app.route('/ping')
def ping():
    with service_rpc_proxy('ping_service') as rpc:
        message = rpc.ping()
    return json.dumps(message)


@app.route('/pong')
def pong():
    with service_rpc_proxy('pong_service') as rpc:
        message = rpc.pong()
    return json.dumps(message)


if __name__ == '__main__':
    app.run()
