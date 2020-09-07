# Kafka Ping-Pong Demo

This repository contains the source for an [Apache Kafka](https://kafka.apache.org/) 2 service _Ping-Pong_ demo.

## Pre-requisites

* `docker`
* `docker-compose`
* `python (>=3.8)`
* `virtualenv`

## Running Tests

#### Unit Tests

A helper script has been created to run the unit-tests for all services within the `services/` folder.

```shell script
./unit-tests.sh
```

This creates a `virtualenv` per service, installs dependencies, runs tests and finally purges the `virtualenv` on completion.

#### Integration Tests

The following command runs automated [`behave`](https://behave.readthedocs.io/en/latest/tutorial.html) tests against the running services in the demo.
On success or failure, the `docker-compose` process will teardown services and return the exit code from the tests.

```shell script
docker-compose up --abort-on-container-exit --exit-code-from integration-tests
```

## Running Demo

To get started simply:

```shell script
docker-compose up
```

You can then perform a `GET` (or visit in a browser) to the following locations:
 * `http://localhost:8080/ping` 
OR
 * `http://localhost:8080/pong`
To start a round of ping-pong.

In the `docker-compose` terminal output, you should be able to see the `ping` and `pong` services consuming messages, 
processing them and producing new messages onto their counterpart's topics:

```shell script
pong_1       | Handling Message: {'message': 'ping', 'uuid': 'e95db462-f0f1-11ea-81e4-0242ac130005'}
rabbit_1     | 2020-09-07 10:07:18.272 [info] <0.1305.0> closing AMQP connection <0.1305.0> (172.19.0.7:33358 -> 172.19.0.2:5672, vhost: '/', user: 'user')
api_1        | 172.19.0.1 - - [07/Sep/2020 10:07:18] "GET /ping HTTP/1.1" 200 -
pong_1       | <BrokerConnection node_id=bootstrap-0 host=kafka:9092 <connecting> [IPv4 ('172.19.0.4', 9092)]>: connecting to kafka:9092 [('172.19.0.4', 9092) IPv4]
pong_1       | Probing node bootstrap-0 broker version
pong_1       | <BrokerConnection node_id=bootstrap-0 host=kafka:9092 <connecting> [IPv4 ('172.19.0.4', 9092)]>: Connection complete.
pong_1       | Broker version identified as 1.0.0
pong_1       | Set configuration api_version=(1, 0, 0) to skip auto check_version requests on startup
pong_1       | Producing Message: {'message': 'pong', 'uuid': 'e95db462-f0f1-11ea-81e4-0242ac130005', 'deliveries': 1}, Topic: ping
pong_1       | <BrokerConnection node_id=1001 host=kafka:9092 <connecting> [IPv4 ('172.19.0.4', 9092)]>: connecting to kafka:9092 [('172.19.0.4', 9092) IPv4]
pong_1       | <BrokerConnection node_id=1001 host=kafka:9092 <connecting> [IPv4 ('172.19.0.4', 9092)]>: Connection complete.
pong_1       | <BrokerConnection node_id=bootstrap-0 host=kafka:9092 <connected> [IPv4 ('172.19.0.4', 9092)]>: Closing connection. 
pong_1       | Closing the Kafka producer with 9223372036.0 secs timeout.
pong_1       | <BrokerConnection node_id=1001 host=kafka:9092 <connected> [IPv4 ('172.19.0.4', 9092)]>: Closing connection. 
ping_1       | Handling Message: {'message': 'pong', 'uuid': 'e95db462-f0f1-11ea-81e4-0242ac130005', 'deliveries': 1}
```