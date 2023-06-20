import argparse
from kafka_producer import KafkaProducer

from transaction_generator import TransactionGenerator



def produce_events(number_of_events: int):
    list_transaction = TransactionGenerator.generate(
        number_of_events=number_of_events)
    KafkaProducer.send_events(list_transaction=list_transaction)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="'Transaction event producer'")
    parser.add_argument('-n', '--number-of-events', type=int,
                        default=1, help="Number of events")
    args = parser.parse_args()
    produce_events(args.number_of_events)
