from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from builder.user_builder import UserBuilder
from builder.wallet_builder import WalletBuilder
from core.models import User
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestCreateMenuAPI(TestCase):

    def test_create_transaction(self):
        user = UserBuilder().build()
        wallet = WalletBuilder().with_balance(100).build()
        query = '''
            mutation createTransaction(
              $text: String!,
              $wallet: ID!,
              $amount: Decimal
            ) {
              createTransaction(
                input: {
                  text: $text,
                  wallet: $wallet,
                  amount: $amount
                }
              ) {
                transaction { id, text, amount, wallet {id, name, balance} }
              }
            }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "text": "Cena con amici",
            "wallet": wallet.id,
            "amount": 10.00
        })
        self.assertNotIn('errors', response)
        transaction = response['data']['createTransaction']['transaction']
        self.assertEqual(transaction['text'], "Cena con amici")
        self.assertEqual(transaction['amount'], '10')
        self.assertEqual(transaction['wallet']['id'], str(wallet.id))
        self.assertEqual('90.00', transaction['wallet']['balance'])


    def test_create_inflow_transaction(self):
        user = UserBuilder().build()
        wallet = WalletBuilder().with_balance(100).build()
        query = '''
            mutation createTransaction(
              $text: String!,
              $wallet: ID!,
              $amount: Decimal,
              $flow: FlowType!
            ) {
              createTransaction(
                input: {
                  text: $text,
                  wallet: $wallet,
                  amount: $amount,
                  flow: $flow
                }
              ) {
                transaction { id, text, amount, wallet {id, name, balance} }
              }
            }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "text": "Cena con amici",
            "wallet": wallet.id,
            "amount": 10.00,
            "flow": "inflow"
        })
        print(response)

