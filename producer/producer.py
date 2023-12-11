#!/usr/bin/env python
import pika

# when RabbitMQ is running on localhost
#params = pika.ConnectionParameters('localhost')

# when RabbitMQ broker is running on network
#params = pika.ConnectionParameters('rabbitmq')

# when starting services with docker compose
params = pika.ConnectionParameters(
    'rabbitmq-demo-rabbitmq-1',
    heartbeat=0)

# create the connection to broker
connection = pika.BlockingConnection(params)
channel = connection.channel()

# create the queue, if it doesn't already exist
channel.queue_declare(queue='messages')

# send a simple message
channel.basic_publish(exchange='',
                      routing_key='messages',
                      body='Hello!')

# log message sending
print("Message sent")

