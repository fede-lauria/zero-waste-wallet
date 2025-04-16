import graphene
from graphene_django import DjangoObjectType

from core.models import User, Transaction
from core.models.wallet import Wallet


class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'balance', 'user']

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
        fields = ['id', 'text', 'amount', 'user', 'wallet', 'flow']


class FlowType(graphene.Enum):
    inflow = 2
    outflow = 1
