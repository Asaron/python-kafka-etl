from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

from clikhouse_sink import ClickhouseSink
from transaction import dict_to_transaction

with open("schema/transaction.avsc") as f:
    SCHEMA_STR = f.read()

SCHEMA_REGISTRY_CONF = {'url': "http://localhost:8081"}
SCHEMA_REGISTRY_CLIENT = SchemaRegistryClient(SCHEMA_REGISTRY_CONF)

AVRO_DESERIALISER = AvroDeserializer(SCHEMA_REGISTRY_CLIENT,
                                     SCHEMA_STR,
                                     dict_to_transaction)

CONSUMER_CONF = {'bootstrap.servers': "localhost:9092",
                 'group.id': "default",
                 'auto.offset.reset': "earliest"}
TOPIC = "transaction"

consumer = Consumer(CONSUMER_CONF)
consumer.subscribe([TOPIC])

TABLE = "transaction"


def consume_events():
    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            record = consumer.poll(1.0)
            if record is None:
                continue
            transaction = AVRO_DESERIALISER(
                record.value(), SerializationContext(record.topic(), MessageField.VALUE))
            if transaction is not None:
                data = [
                    str(transaction.metadata.event_id), 
                    str(transaction.metadata.timestamp), 
                    str(transaction.payload.consumer_id),
                    str(transaction.payload.bank_id),
                    transaction.payload.amount,
                    str(transaction.payload.country_code),
                    str(transaction.payload.execution_date),
                    str(transaction.payload.merchant_id)]
                print(data)
                ClickhouseSink.insert_rows(table=TABLE, data=data)
                    
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == "__main__":
    consume_events()
