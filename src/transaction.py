class Transaction(object):
    """
    Transaction record

    Args:
        metadata (str): Transaction's metadata

        payload (int): Transaction's payload
    """

    def __init__(self, metadata: dict, payload: dict) -> None:
        self.metadata = self.Metadata(
            metadata["event_id"], metadata["timestamp"])
        self.payload = self.Payload(payload["consumer_id"],
                                    payload["bank_id"],
                                    payload["amount"],
                                    payload["country_code"],
                                    payload["execution_date"],
                                    payload["merchant_id"])

    class Metadata(object):
        """
        Metadata record

        Args:
            event_id (str): Transaction's unique identifier

            timestamp (int): Transaction's ingestion timestamp
        """

        def __init__(self, event_id, timestamp) -> None:
            self.event_id = event_id
            self.timestamp = timestamp

    class Payload(object):
        """
        Metadata record

        Args:
            consumer_id (str): Connsumer's unique identifier

            bank_id (str): Bank's unique identifier

            amount (str): Transaction's amount

            country_code (str): Transaction's country of origin 

            execution_date (str): Execution date of the transaction

            merchant_id (str): merchant's unique identifier
        """

        def __init__(self, consumer_id, bank_id, amount, country_code, execution_date, merchant_id) -> None:
            self.consumer_id = consumer_id
            self.bank_id = bank_id
            self.amount = amount
            self.country_code = country_code
            self.execution_date = execution_date
            self.merchant_id = merchant_id


def transaction_to_dict(transaction: Transaction, ctx) -> dict:
    """
    Returns a dict representation of a Transaction instance for serialization.

    Args:
        transaction (Transaction): Transaction instance.

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        dict: Dict populated with user attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    return dict(metadata=dict(event_id=transaction.metadata.event_id,
                              timestamp=transaction.metadata.timestamp),
                payload=dict(consumer_id=transaction.payload.consumer_id,
                             bank_id=transaction.payload.bank_id,
                             amount=transaction.payload.amount,
                             country_code=transaction.payload.country_code,
                             execution_date=transaction.payload.execution_date,
                             merchant_id=transaction.payload.merchant_id))


def dict_to_transaction(object, ctx) -> Transaction:
    """
    Converts object literal(dict) to a Transaction instance.

    Args:
        obj (dict): Object literal(dict)

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    """

    if object is None:
        return None

    return Transaction(metadata=object["metadata"],
                       payload=object["payload"])
