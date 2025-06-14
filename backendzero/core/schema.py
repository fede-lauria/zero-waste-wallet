from decimal import Decimal

import graphene
from django.db import models
from graphene_django_cud.mutations import DjangoCreateMutation

from core.mixins.auth_graphql import permissions, is_logged
from core.models import Transaction, Currency, Patients, ProgressiveVisit
from core.models.wallet import Wallet
from core.schema_type import WalletType, TransactionType, WalletsTotalBalanceType, CurrencyType, PatientsType, \
    ProgressiveVisitType


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
        wallet = Wallet.objects.get(id=input['wallet'])
        flow = input['flow']
        if flow == 1:
            wallet.add_amount(obj.amount)
        else:
            wallet.remove_amount(obj.amount)


class CreateWalletMutation(DjangoCreateMutation):
    class Meta:
        model = Wallet
        login_required = True
        exclude_fields = 'user'

    @classmethod
    @permissions(is_logged)
    def before_mutate(self, root, info, input):
        user = info.context.user
        input['user'] = user.id
        return input

class CreatePatientMutation(DjangoCreateMutation):
    class Meta:
        model = Patients
        login_required = True
        exclude_fields = 'user'

    @classmethod
    @permissions(is_logged)
    def before_mutate(self, root, info, input):
        user = info.context.user
        input['user'] = user.id
        return input

class CreateProgressiveVisitMutation(DjangoCreateMutation):
    class Meta:
        model = ProgressiveVisit
        login_required = True
        exclude_fields = 'user'

    @classmethod
    @permissions(is_logged)
    def before_mutate(self, root, info, input):
        user = info.context.user
        input['user'] = user.id
        return input

class GetBmiMutation(graphene.Mutation):
    class Arguments:
        patient = graphene.ID()
        weight = graphene.Float()

    bmi = graphene.Float()

    @permissions(is_logged)
    def mutate(self, info, patient, weight):
        user = info.context.user
        patient = Patients.objects.filter(id=patient, user=user).first()
        if not patient:
            raise Exception("User not authorized")
        height = patient.height

        if weight is None:
            raise Exception("Weight is required")

        if weight == 0:
            raise Exception("Weight cannot be 0")

        if height is None:
            raise Exception("Height is required")

        bmi = round(weight / (float((height / 100 )) ** 2), 2)

        return GetBmiMutation(bmi=bmi)


class Mutation(graphene.ObjectType):
    create_transaction = CreateTransactionMutation.Field()
    create_wallet = CreateWalletMutation.Field()
    create_patient = CreatePatientMutation.Field()
    create_progressive_visit = CreateProgressiveVisitMutation.Field()
    get_bmi = GetBmiMutation.Field()


class Query(graphene.ObjectType):
    wallets = graphene.List(WalletType)
    wallet = graphene.Field(WalletType, id=graphene.Int())
    wallets_total_balance = graphene.Field(WalletsTotalBalanceType)
    transactions = graphene.List(TransactionType)
    transaction = graphene.Field(TransactionType, id=graphene.Int())
    transactions_by_wallet = graphene.List(TransactionType, id=graphene.Int())
    currency = graphene.List(CurrencyType)
    patients = graphene.List(PatientsType)
    progressive_visit_by_patient = graphene.List(ProgressiveVisitType, id=graphene.Int())

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

    def resolve_progressive_visit_by_patient(self, info, id):
        user = info.context.user
        return ProgressiveVisit.objects.filter(patient=id, user=user)

    @permissions(is_logged)
    def resolve_wallets_total_balance(self, info):
        user = info.context.user
        total = Wallet.objects.filter(user=user).aggregate(total=models.Sum('balance'))['total'] or 0
        return WalletsTotalBalanceType(total_balance=float(total), user_id=user.id)

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

    @permissions(is_logged)
    def resolve_currency(self, info):
        return Currency.objects.all()

    def resolve_patients(self, info):
        user = info.context.user
        return Patients.objects.filter(user=user)





schema = graphene.Schema(query=Query, mutation=Mutation)