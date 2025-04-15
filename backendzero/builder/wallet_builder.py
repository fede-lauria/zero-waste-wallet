from builder.user_builder import UserBuilder
from core.models import Wallet
from model_bakery import baker

class WalletBuilder:
    def __init__(self):
        self.balance = 0
        self.name = 'test'
        self.user = None

    def with_user(self, user):
        self.user = user
        return self

    def with_balance(self, balance):
        self.balance = balance
        return self

    def with_name(self, name):
        self.name = name
        return self

    def build(self):
        if self.user is None:
            self.user = UserBuilder().build()
        wallet = baker.make(Wallet, name=self.name, user=self.user, balance=self.balance)
        return wallet