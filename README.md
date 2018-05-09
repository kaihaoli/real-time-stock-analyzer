# Real Time Stock Analyzer
Real time stock price visualization by using **bigdata pipeline**.

## Step 0. Set up Environment
Using Docker Machine "bigdata".
* 1 [Run zookeeper, Kafka using Docker](https://kaihaoli.github.io/2018/04/25/docker-quick-start/)
  * Enter "bigdata" docker machine
  ```sh
  > eval $(docker-machine env bigdata)
  ```
* 2 Docker Start zookeeper, kafka, cassandra, redis
```sh
> ./local-setup.sh
```

## Step 1. Kafka
```sh
> eval $(docker-machine env bigdata)
```
### Create Topic
```sh
> cd cd opt/kafka_2.xx-x.xx.x.x/
```
* Stock Price topic "stock-analyzer"
```sh
> bin/kafka-topics.sh --create \
                      --zookeeper zookeeper:2181 \
                      --replication-factor 1 \
                      --partitions 1 \
                      --topic stock-analyzer
```
### Data Producer
* realtime data from googlefinance  
* write data to Kafka topic "stock-analyzer" as producer


## Step 2. Cassandra
* Kafka data consumer
* Store Data to Cassandra database

## Step 3. Spark
### Create Kafka Topic
* Kafka Average Stock Price topic "average-stock-price"
```sh
# kafka directory
> bin/kafka-topics.sh --create \
                      --zookeeper zookeeper:2181 \
                      --replication-factor 1 \
                      --partitions 1 \
                      --topic average-stock-price
```
* Kafka data topic "stock-analyzer" consumer
* Spark Streaming calculate Average price
* write to another kafka topic "average-stock-price"
