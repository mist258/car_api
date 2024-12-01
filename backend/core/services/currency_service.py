from decimal import Decimal

import requests


class CurrencyService:

    @staticmethod
    def get_exchange_rates():
        res = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')

        if res.status_code == 200:
            data = res.json()
            rates = {}

            for rate in data:

                if rate.get('ccy') in ['USD', 'EUR']:
                    rates[rate['ccy']] = {
                        'sale': Decimal(str(rate['sale'])),
                        'purchase': Decimal(str(rate['buy'])),
                    }
            return rates

        return None
