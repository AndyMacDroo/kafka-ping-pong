import os

from behave import *
import requests


@given("we have a running Ping-Pong API")
def step_impl(context):
    r = requests.get('http://%s:%s/' % (os.getenv('API_HOST'), os.getenv('API_PORT')))
    assert r.status_code == 200
    assert r.text == "Hello World!"


@when(u"I make a request to {path}")
def step_impl(context, path):
    context.request = requests.get('http://%s:%s/%s' % (os.getenv('API_HOST'), os.getenv('API_PORT'), path))


@then(u"I receive a {status_code} status code and a non empty body returned")
def step_impl(context, status_code):
    assert context.request.status_code == int(status_code)
    assert context.request.json() is not None
