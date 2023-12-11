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

# define a function to call when message is received
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# setup to listen for messages on queue 'messages'
channel.basic_consume(queue='messages',
                      auto_ack=True,
                      on_message_callback=callback)

# log message to show we've started
print('Waiting for messages. To exit press CTRL+C')

# start listening
channel.start_consuming()
