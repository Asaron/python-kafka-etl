from confluent_kafka import Consumer

from clikhouse_sink import ClickhouseSink
from deserializer import Deserializer

from datetime import datetime

CONSUMER_CONF = {'bootstrap.servers': "localhost:9092",
                 'group.id': "default",
                 'auto.offset.reset': "earliest"}
TOPIC = "transaction"

CONSUMER = Consumer(CONSUMER_CONF)
CONSUMER.subscribe([TOPIC])

TABLE = "transaction"


def consume_events():
    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            record = CONSUMER.poll(1.0)
            if record is None:
                continue
            transaction = Deserializer.deserialize(record=record)
            if transaction is not None:
                data = create_data_structure(transaction=transaction)
                ClickhouseSink.insert_rows(table=TABLE, data=data)

        except KeyboardInterrupt:
            break

    CONSUMER.close()


def create_data_structure(transaction):
    return [
        str(transaction.metadata.event_id),
        datetime.fromtimestamp(float(transaction.metadata.timestamp)),
        str(transaction.payload.consumer_id),
        str(transaction.payload.bank_id),
        transaction.payload.amount,
        str(transaction.payload.country_code),
        str(transaction.payload.execution_date),
        str(transaction.payload.merchant_id)
    ]


if __name__ == "__main__":
    consume_events()
