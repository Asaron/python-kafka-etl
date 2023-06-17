# python-kafka-etl

## Installation

Create topic:

```bash
docker exec broker \
kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic transaction
```