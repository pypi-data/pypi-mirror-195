# Confluent CLI Wraper for Python

Simple wrapper library to Confluent CLI


## Get started

```bash
poetry add python-confluent-cli-wrapper
```

```python
from confluent.cli.wrapper.environment import Environment
from confluent.cli.wrapper.kafka_cluster import KafkaCluster
from confluent.cli.wrapper.kafka_topic import KafkaTopic
from confluent.cli.wrapper.session import login
from confluent.cli.wrapper.utils.parsers import OutputEnum

environment=Environment()
kafka_cluster=KafkaCluster()
kafka_topic=KafkaTopic()

login()

environment.list()

kafka_cluster.list()  # eq '--all' argument

```
