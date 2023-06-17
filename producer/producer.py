
import io
import uuid
from datetime import datetime

import avro.schema
from avro.io import DatumWriter

SCHEMA = avro.schema.parse(open("event/transaction.avsc", "rb").read())


def produce_events():
    writer = DatumWriter(SCHEMA)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    event = {
        "metadata": {
            "event_id": str(uuid.uuid4()), 
            "timestamp": str(datetime.timestamp(datetime.now()))
            },
        "payload": {
            "consumer_id": str(uuid.uuid4()),
            "bank_id": str(uuid.uuid4()),
            "amount": 1.0,
            "country_code": "FR", 
            "execution_date": datetime.now().isoformat(),
            "merchant_id": str(uuid.uuid4()),
            }
        }
    writer.write(event, encoder)
    raw_bytes = bytes_writer.getvalue()


if __name__ == "__main__":
    produce_events()
