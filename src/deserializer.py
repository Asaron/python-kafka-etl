from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext

from transaction import dict_to_transaction

with open("schema/transaction.avsc") as f:
    SCHEMA_STR = f.read()

SCHEMA_REGISTRY_CONF = {'url': "http://localhost:8081"}
SCHEMA_REGISTRY_CLIENT = SchemaRegistryClient(SCHEMA_REGISTRY_CONF)

AVRO_DESERIALISER = AvroDeserializer(SCHEMA_REGISTRY_CLIENT,
                                     SCHEMA_STR,
                                     dict_to_transaction)


class Deserializer:

    @staticmethod
    def deserialize(record):
        return AVRO_DESERIALISER(record.value(), SerializationContext(record.topic(), MessageField.VALUE))
