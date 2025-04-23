
from model_bakery import baker

from core.models import Currency


class CurrencyBuilder:
    def __init__(self):
        self.name = 'EUR'
        self.symbol = '€'

    def with_name(self, name):
        self.name = name
        return self

    def with_symbol(self, symbol):
        self.symbol = symbol
        return self

    def build(self):
        currency = baker.make(Currency, name=self.name, symbol=self.symbol)
        return currency