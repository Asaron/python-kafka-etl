import uuid

from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (MessageField, SerializationContext,
                                           StringSerializer)

from transaction import Transaction, transaction_to_dict

with open("schema/transaction.avsc") as f:
    SCHEMA_STR = f.read()
SCHEMA_REGISTRY_CONF = {'url': "http://localhost:8081"}
SCHEMA_REGISTRY_CLIENT = SchemaRegistryClient(SCHEMA_REGISTRY_CONF)
AVRO_SERIALISER = AvroSerializer(SCHEMA_REGISTRY_CLIENT,
                                 SCHEMA_STR,
                                 transaction_to_dict)
STRING_SERIALIZER = StringSerializer('utf_8')

PRODUCER_CONF = {'bootstrap.servers': "localhost:9092"}
PRODUCER = Producer(PRODUCER_CONF)
TOPIC = "transaction"


class KafkaProducer:

    @staticmethod
    def send_events(list_transaction: list[Transaction]) -> None:
        for transaction in list_transaction:
            PRODUCER.produce(topic=TOPIC,
                             key=STRING_SERIALIZER(str(uuid.uuid4())),
                             value=AVRO_SERIALISER(transaction, SerializationContext(
                                 TOPIC, MessageField.VALUE)),
                             on_delivery=delivery_report)
        PRODUCER.flush()


def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.

        msg (Message): The message that was produced or failed.

    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.
    """

    if err is not None:
        print("Delivery failed for Transaction record {}: {}".format(
            msg.key(), err))
        return
    print('Transaction record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))
