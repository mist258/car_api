from datetime import datetime
from decimal import Decimal

import requests


class CurrencyService:

    @staticmethod
    def get_exchange_rates():
        res = requests.get(
            f'https://api.privatbank.ua/p24api/exchange_rates?date={datetime.now().strftime('%d.%m.%Y')}'
        )

        if res.status_code == 200:
            data = res.json()
            rates = {}

            for rate in data['exchangeRate']:
                if rate.get('currency') in ['USD', 'EUR']:
                    rates[rate['currency']] = {
                        'sale': Decimal(str(rate['saleRate'])),
                        'purchase': Decimal(str(rate['purchaseRate'])),
                    }

            return rates

        return None
