Feature: Kafka Ping Pong

  Background:
    Given we have a running Ping-Pong API

  Scenario: Ping-Pong API returns response delegated to ping service
    When I make a request to ping
    Then I receive a 200 status code
    And the response has a message property with value ping

  Scenario: Ping-Pong API returns response delegated to pong service
    When I make a request to pong
    Then I receive a 200 status code
    And the response has a message property with value pong