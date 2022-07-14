import requests
import json
from config import keys


class ConvertionExeption(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExeption(f'Невозможно перевести одинаковые валюты {base} \n')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Неверное название валюты {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Неверное название валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Неверное количество валюты {amount},')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base
