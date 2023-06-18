
import argparse
import uuid
from datetime import datetime
import random

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import pycountry

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


def produce_events(number_of_events: int):
    country_codes = list(pycountry.countries)
    for _ in range(0, number_of_events):
        country = random.choice(country_codes)
        transaction = Transaction(dict(event_id=str(uuid.uuid4()), timestamp=str(datetime.timestamp(datetime.now()))),
                                    dict(consumer_id=str(uuid.uuid4()),
                                        bank_id=str(uuid.uuid4()),
                                        amount=round(random.uniform(1, 1000), 2),
                                        country_code=country.alpha_2,
                                        execution_date=datetime.now().isoformat(),
                                        merchant_id=str(uuid.uuid4()))
                                    )
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
        print("Delivery failed for Transaction record {}: {}".format(msg.key(), err))
        return
    print('Transaction record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="'Transaction event producer'")
    parser.add_argument('-n', '--number-of-events', type=int, default=1, help="Number of events")
    args = parser.parse_args()
    produce_events(args.number_of_events)
