import random
import uuid
from datetime import datetime

import pycountry

from transaction import Transaction


class TransactionGenerator:

    @staticmethod
    def generate(number_of_events: int) -> list[Transaction]:
        country_codes = list(pycountry.countries)
        transaction = []
        for _ in range(0, number_of_events):
            country = random.choice(country_codes)
            transaction.append(Transaction(dict(event_id=str(uuid.uuid4()), timestamp=str(datetime.timestamp(datetime.now()))),
                                           dict(consumer_id=str(uuid.uuid4()),
                                                bank_id=str(uuid.uuid4()),
                                                amount=round(
                                                    random.uniform(1, 1000), 2),
                                                country_code=country.alpha_2,
                                                execution_date=datetime.now().isoformat(),
                                                merchant_id=str(uuid.uuid4()))
                                           ))
        return transaction
