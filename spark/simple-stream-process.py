import atexit
import logging
import json
import sys
import time

# Kafka
from kafka import KafkaProducer

# Python Spark
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('stream-processing')
logger.setLevel(logging.INFO)

def shutdown_hook(producer):
    """
    a shutdown hook to be called before the shutdown
    :param producer: instance of a kafka producer
    :return: None
    """
    try:
        logger.info('Flushing pending messages to kafka, timeout is set to 10s')
        producer.flush(10)
        logger.info('Finish flushing pending messages to kafka')
    except KafkaError as kafka_error:
        logger.warn('Failed to flush pending messages to kafka, caused by: %s', kafka_error.message)
    finally:
        try:
            logger.info('Closing kafka connection')
            producer.close(10)
        except Exception as e:
            logger.warn('Failed to close kafka connection, caused by: %s', e.message)

def process_stream(stream):

    def send_to_kafka(rdd):
        results = rdd.collect()
        for r in results:
            data = json.dumps(
                {
                    'symbol': r[0],
                    'timestamp': time.time(),
                    'average': r[1]
                }
            )
            try:
                logger.info('Sending average price %s to kafka' % data)
                kafka_producer.send(target_topic, value=data)
            except KafkaError as error:
                logger.warn('Failed to send average stock price to kafka, caused by: %s', error.message)

    def pair(data):
        record = json.loads(data[1].decode('utf-8'))
        return record.get('StockSymbol'), (float(record.get('LastTradePrice')), 1)

    # Stream Calculation
    stream.map(pair) \
          .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
          .map(lambda (k, v): (k, v[0]/v[1])) \
          .foreachRDD(send_to_kafka)


if __name__ == '__main__':
    # Kafka Configuration
    # "stock-analyzer", "average-stock-price"
    topic = "test"
    target_topic = "stock-analyzer"
    brokers = "192.168.99.100:9092"

    # Spark
    # 1 Create SparkContext and StreamingContext
    sc = SparkContext("local[2]", "StockAveragePrice") # (master, appName)
    sc.setLogLevel('ERROR')
    # Batch Duration Time = 5
    ssc = StreamingContext(sc, 5)

    # 2 Instantiate a kafka stream for processing
    # Kafka Data Consumer
    directKafkaStream = KafkaUtils.createDirectStream(
                                ssc,
                                [topic],
                                {'metadata.broker.list': brokers})
    process_stream(directKafkaStream)

    # 3 Instantiate a simple kafka producer
    kafka_producer = KafkaProducer(
        bootstrap_servers=brokers
    )

    # setup proper shutdown hook
    atexit.register(shutdown_hook, kafka_producer)

    # Spark Streaming Start
    ssc.start()
    ssc.awaitTermination()
