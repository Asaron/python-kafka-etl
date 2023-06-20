import clickhouse_connect

CLIENT = clickhouse_connect.get_client(host='localhost', username='etl', password='password')

class ClickhouseSink:

    @staticmethod
    def insert_rows(table: str, data: object):
        CLIENT.insert(table, [data], column_names=[
            "event_id",
            "timestamp",
            "consumer_id",
            "bank_id",
            "amount",
            "country_code",
            "execution_date",
            "merchant_id"
            ])

    
