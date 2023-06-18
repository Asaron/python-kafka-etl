# python-kafka-etl

## Installation

### Start Kafka cluster:
```bash
docker-compose up -d --remove-orphans
```


### Create topic:
```bash
docker exec broker \
kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic transaction
```

### Create a new Avro schema:
Create a new Avro schema file in `event/`

Then, to send schema to Schema Registry:
```bash
sh utils/send_schema_to_schema_registry.sh schema-name
```