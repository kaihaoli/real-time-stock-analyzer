'''
# Connect to any kafka broker
# Fetch stock price every second
'''
import time
import datetime
import random
import logging
import atexit
import schedule
import json

# Google Finance Real Time Data
from googlefinance import getQuotes

# Import kafka python client
from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError

# Kafka
# - default kafka topic to write to
topic_name = 'test'
#'stock-analyzer'
# - default kafka broker location
kafka_broker = '192.168.99.100:9092'
#'127.0.0.1:9092'

# - logging configuration
import logging
logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)

def fetch_stock_price(producer, symbol):
    """
    helper function to retrieve stock data and send it to kafka
    :param producer: instance of a kafka producer
    :param symbol: symbol of the stock
    :return: None
    """
    logger.debug('Start to fetch stock price for %s', symbol)
    try:
        #payload = price = json.dumps(getQuotes(symbol))
        price = random.randint(30, 120) # random price
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%MZ')
        val = {"StockSymbol": symbol, "LastTradePrice":price, "LastTradeDateTime":timestamp}
        payload = json.dumps(val, encoding="utf-8")
        #payload = json.dumps(('[{"StockSymbol":%s,"LastTradePrice":%d,"LastTradeDateTime":"%s"}]' % (symbol, price, timestamp)).encode('utf-8'))
        logger.debug('Retrieved stock info %s', price)
        future = producer.send(topic=topic_name, value=payload)
        #future = producer.send(topic=topic_name, value=payload, timestamp_ms=time.time())
        logger.debug('Sent stock price for %s to Kafka', symbol)
    except KafkaTimeoutError as timeout_error:
        logger.warn('Failed to send stock price for %s to kafka, caused by: %s', (symbol, timeout_error.message))
    except Exception:
        print Exception
        logger.warn('Failed to fetch stock price for %s', symbol)

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

if __name__ == '__main__':
    symbol = 'AAPL'

    # 1 Instantiate a Simple kafka producer
    producer = KafkaProducer(
        bootstrap_servers = kafka_broker
    )

    # 2 Schedule and run the fetch_stock_price function every second
    schedule.every(1).second.do(fetch_stock_price, producer, symbol)

    # 3 Setup proper shutdown hook
    atexit.register(shutdown_hook, producer)

    while True:
        schedule.run_pending()
        time.sleep(1)
'''
    for _ in range(10):
        future = producer.send(topic='test', value=b'some_message_bytes')
        #future = producer.send('foobar', b'another_message')
        result = future.get(timeout=60)
        print result
'''
