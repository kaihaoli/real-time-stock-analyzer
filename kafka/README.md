# Kafka

## Dependencies
```bash
> pip install -r requirements.txt
```
* [googlefinance](https://github.com/hongtaocai/googlefinance)
  * Python module to get stock data from Google Finance API
  * This module provides **no delay, real time** stock data in NYSE & NASDAQ.
* [kafka-python](https://github.com/dpkp/kafka-python)
  * Python client for the Apache Kafka distributed stream processing system. kafka-python is designed to function much like the official java client, with a sprinkling of pythonic interfaces (e.g., consumer iterators).
* [schedule](https://github.com/dbader/schedule)
  * Schedule lets you run Python functions (or any other callable) periodically at pre-determined intervals using a simple, human-friendly syntax.

## Virtual env
```bash
> eval $(docker-machine env bigdata)
```
### Create Kafka Topic
``` bash
# Enter the container 'kafka'
> docker exec -it kafka /bin/bash
# Change to the kafka default directory
> cd /opt/kafka_2.12-1.1.0/
# Create a Topic 'stock'
> bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic stock
```
