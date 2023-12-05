# rabbitmq-demo
Demo of RabbitMQ consumer/producer

## Communicate between python processes

For this exercise, ensure both consumer.py and producer.py use the 'localhost' broker address

First start the RabbitMQ broker
```
docker run --rm -d -p 15672:15672 -p 5672:5672 --name rabbitmq rabbitmq:3-management
```

Now run the consumer in one terminal
```
python consumer/consumer.py
```

And the producer in another
```
python producer/producer.py
```

## Containers example

Now change consumer.py and producer.py to use the 'rabbitmq' broker address, and build both containers
```
docker image build -t producer producer/.
docker image build -t consumer consumer/.
```

Create a network for your containers to communicate
```
docker network create rabbit
```

Start the RabbitMQ broker (this time attaching the 'rabbit' network)
```
docker run --rm -d -p 15672:15672 -p 5672:5672 --network rabbit --name rabbitmq rabbitmq:3-management
```

And then your containers - in two separate terminals, so you can run the consumer interactively
```
docker run --rm -it --network rabbit --name consumer
docker run --rm -d --network rabbit --name producer
```

## Swarm services example

When starting services manually, as here, the broker address will remain 'rabbitmq'.

First start your swarm
```
docker swarm init
```

Create the network (overlay this time)
```
docker network create --driver overlay rabbit
```

And then start the services
```
docker service create -p 15672:15672 -p 5672:5672 --network rabbit --name rabbitmq rabbitmq:3-management
docker service create --network rabbit --name consumer consumer
docker service create --network rabbit --name producer producer
```

## Docker compose example

The docker-compose.yml file defines three services for the broker, consumer and producer. The startup sequence is controlled by introducing a 'healthcheck' for the rabbitmq service, and delaying start of the consumer and producer until this healthcheck is satisfied.  The consumer and producer are also replicated.

Note that when running under compose, the service names are modified, so the address used by consumer and producer needs to be modified to 'rabbitmq-demo-rabbitmq-1'.

To start everything simply run :
```
docker compose up
```