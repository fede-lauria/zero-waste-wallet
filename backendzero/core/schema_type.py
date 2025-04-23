import graphene
from graphene_django import DjangoObjectType

from core.models import User, Transaction, Currency
from core.models.wallet import Wallet


class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'balance', 'user', 'currency']

class WalletsTotalBalanceType(graphene.ObjectType):
    total_balance = graphene.Float()
    user_id = graphene.Int()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ['id', 'text', 'amount', 'user', 'wallet', 'flow', 'day']

class CurrencyType(DjangoObjectType):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'symbol']


