from kafka import KafkaConsumer

import argparse
import atexit
import logging
import redis

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('redis-publisher')
logger.setLevel(logging.DEBUG)


def shutdown_hook(kafka_consumer):
    """
    a shutdown hook to be called before the shutdown
    :param kafka_consumer: instance of a kafka consumer
    :return: None
    """
    logger.info('Shutdown kafka consumer')
    kafka_consumer.close()


if __name__ == '__main__':
    # Init Argument
    topic_name = "average-stock-price"
    kafka_broker = "192.168.99.100:9092"
    redis_channel = "average-stock-price"
    redis_host = "192.168.99.100"
    redis_port = "6379"

    # 1 Instantiate a simple kafka consumer
    kafka_consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=kafka_broker
    )

    # 2 Instantiate a redis client
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

    # 3 Setup proper shutdown hook
    atexit.register(shutdown_hook, kafka_consumer)

    # 4 Publish Redis 
    for msg in kafka_consumer:
        logger.info('Received new data from kafka %s' % str(msg))
        redis_client.publish(redis_channel, msg.value)
