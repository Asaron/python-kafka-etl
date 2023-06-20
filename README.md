# python-kafka-etl

## Installation

### Kafka 

#### Start Kafka cluster:
```bash
docker-compose up -d --remove-orphans
```


#### Create topic:
```bash
docker exec broker \
kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic transaction
```

#### Create a new Avro schema:
Create a new Avro schema file in `event/`

Then, to send schema to Schema Registry:
```bash
sh utils/send_schema_to_schema_registry.sh schema-name
```

### Python
Create a python environment with Pyenv:
```bash
pyenv virtualenv 3.11.0 kafka-python
```

Activate Pyenv:
```bash
pyenv shell kafka-python
```

## Clickhouse
Enter Clickhouse:
```bash
docker exec -it clickhouse-server clickhouse-client
'''
