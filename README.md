# Real Time Stock Analyzer
Real time stock price visualization by using **bigdata pipeline**.

## Step0. Set up Docker Environment
* 1 [Run zookeeper, Kafka using Docker](https://kaihaoli.github.io/2018/04/25/docker-quick-start/)
  * Enter "bigdata" docker machine
  ```sh
  > eval $(docker-machine env bigdata)
  ```
* 2 Docker Start zookeeper, kafka, cassandra
```sh
> ./local-setup.sh
```

## Step1. Kafka
* Create Topic
* Kafka data producer

## Step2. Cassandra
* Kafka data consumer
* Store Data to Cassandra database

## Step3. Spark
* Kafka data consumer
