import graphene
from graphene_django_cud.mutations import DjangoCreateMutation

from core.mixins.auth_graphql import permissions, is_logged
from core.models import Transaction
from core.models.wallet import Wallet
from core.schema_type import WalletType, TransactionType

class CreateTransactionMutation(DjangoCreateMutation):
    class Meta:
        model = Transaction
        login_required = True
        exclude_fields = 'user'

    @classmethod
    def before_mutate(cls, root, info, input):
        user = info.context.user
        input['user'] = user.id
        return input

    @classmethod
    def after_mutate(cls, root, info, input, obj, return_data):
        wallet = obj.wallet
        wallet.remove_amount(obj.amount)


class Mutation(graphene.ObjectType):
    create_transaction = CreateTransactionMutation.Field()


class Query(graphene.ObjectType):
    wallets = graphene.List(WalletType)
    wallet = graphene.Field(WalletType, id=graphene.Int())
    transactions = graphene.List(TransactionType)
    transaction = graphene.Field(TransactionType, id=graphene.Int())
    transactions_by_wallet = graphene.List(TransactionType, id=graphene.Int())

    @permissions(is_logged)
    def resolve_wallets(self, info):
        user = info.context.user
        if user.is_authenticated:
            return Wallet.objects.filter(user=user)
        return []

    @permissions(is_logged)
    def resolve_wallet(self, info, id):
        user = info.context.user
        return Wallet.objects.get(id=id, user=user)

    @permissions(is_logged)
    def resolve_transactions(self, info):
        user = info.context.user
        return Transaction.objects.filter(user=user)

    @permissions(is_logged)
    def resolve_transaction(self, info, id):
        user = info.context.user
        return Transaction.objects.get(id=id, user=user)

    @permissions(is_logged)
    def resolve_transactions_by_wallet(self, info, id):
        user = info.context.user
        return Transaction.objects.filter(wallet=id, user=user)




schema = graphene.Schema(query=Query, mutation=Mutation)