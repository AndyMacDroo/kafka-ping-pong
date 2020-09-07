import os

from behave import *
import requests


@given("we have a running Ping-Pong API")
def step_impl(context):
    r = requests.get('http://%s:%s/' % (os.getenv('API_HOST'), os.getenv('API_PORT')))
    assert r.status_code == 200
    assert r.text == "Hello World!"


@when(u"I make a request to {path}")
def make_a_request(context, path):
    context.response = requests.get('http://%s:%s/%s' % (os.getenv('API_HOST'), os.getenv('API_PORT'), path))


@then(u"I receive a {status_code} status code")
def receive_status_code(context, status_code):
    assert context.response.status_code == int(status_code)


@then(u"the response has a {property} property with value {value}")
def response_has_property_and_value(context, property, value):
    json_response = context.response.json()
    assert json_response[property] == value
