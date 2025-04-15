from builder.user_builder import UserBuilder
from model_bakery import baker

from builder.wallet_builder import WalletBuilder
from core.models import Transaction


class TransactionBuilder:
    def __init__(self):
        self.amount = 0
        self.text = 'Transazione di prova'
        self.user = None
        self.wallet = None

    def with_user(self, user):
        self.user = user
        return self

    def with_amount(self, amount):
        self.amount = amount
        return self

    def with_name(self, text):
        self.text = text
        return self

    def with_wallet(self, wallet):
        self.wallet = wallet
        return self

    def with_text(self, text):
        self.text = text
        return self

    def build(self):
        if self.user is None:
            self.user = UserBuilder().build()
        if self.wallet is None:
            self.wallet = WalletBuilder().with_user(self.user).build()
        wallet = baker.make(Transaction, text=self.text, user=self.user, amount=self.amount, wallet=self.wallet)
        return wallet