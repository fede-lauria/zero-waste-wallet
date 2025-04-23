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
              $amount: Decimal,
              $flow: Int!
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
            "flow": 0
        })
        self.assertNotIn('errors', response)
        transaction = response['data']['createTransaction']['transaction']
        self.assertEqual(transaction['text'], "Cena con amici")
        self.assertEqual(transaction['amount'], '10')
        self.assertEqual(transaction['wallet']['id'], str(wallet.id))
        self.assertEqual('90.00', transaction['wallet']['balance'])


    def test_create_plus_transaction(self):
        user = UserBuilder().build()
        wallet = WalletBuilder().with_balance(100).build()
        query = '''
            mutation createTransaction(
              $text: String!,
              $wallet: ID!,
              $amount: Decimal,
              $flow: Int!
            ) {
              createTransaction(
                input: {
                  text: $text,
                  wallet: $wallet,
                  amount: $amount,
                  flow: $flow
                }
              ) {
                transaction { id, text, amount, flow ,wallet {id, name, balance} }
              }
            }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "text": "Cena con amici",
            "wallet": wallet.id,
            "amount": 10.00,
            "flow": 1
        })

        self.assertNotIn('errors', response)
        transaction = response['data']['createTransaction']['transaction']
        self.assertEqual(transaction['text'], "Cena con amici")
        self.assertEqual(transaction['amount'], '10')
        self.assertEqual(transaction['flow'], 1)
        self.assertEqual(transaction['wallet']['id'], str(wallet.id))
        self.assertEqual('110.00', transaction['wallet']['balance'])

    def test_create_minus_transaction(self):
        user = UserBuilder().build()
        wallet = WalletBuilder().with_balance(100).build()
        query = '''
            mutation createTransaction(
              $text: String!,
              $wallet: ID!,
              $amount: Decimal,
              $flow: Int!
            ) {
              createTransaction(
                input: {
                  text: $text,
                  wallet: $wallet,
                  amount: $amount,
                  flow: $flow
                }
              ) {
                transaction { id, text, amount, flow ,wallet {id, name, balance} }
              }
            }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "text": "Cena con amici",
            "wallet": wallet.id,
            "amount": 10.00,
            "flow": 0
        })

        self.assertNotIn('errors', response)
        transaction = response['data']['createTransaction']['transaction']
        self.assertEqual(transaction['text'], "Cena con amici")
        self.assertEqual(transaction['amount'], '10')
        self.assertEqual(transaction['flow'], 0)
        self.assertEqual(transaction['wallet']['id'], str(wallet.id))
        self.assertEqual('90.00', transaction['wallet']['balance'])


    def test_create_minus_transaction_with_day(self):
        user = UserBuilder().build()
        wallet = WalletBuilder().with_balance(100).build()
        query = '''
            mutation createTransaction(
              $text: String!,
              $wallet: ID!,
              $amount: Decimal,
              $flow: Int!,
              $day: Date!,
              
            ) {
              createTransaction(
                input: {
                  text: $text,
                  wallet: $wallet,
                  amount: $amount,
                  flow: $flow,
                  day: $day
                }
              ) {
                transaction { id, text, amount, day, flow,wallet {id, name, balance} }
              }
            }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "text": "Cena con amici",
            "wallet": wallet.id,
            "amount": 10.00,
            "flow": 0,
            "day": "2025-03-13",
        })

        self.assertNotIn('errors', response)
        transaction = response['data']['createTransaction']['transaction']
        self.assertEqual(transaction['text'], "Cena con amici")
        self.assertEqual(transaction['amount'], '10')
        self.assertEqual(transaction['flow'], 0)
        self.assertEqual(transaction['wallet']['id'], str(wallet.id))
        self.assertEqual('2025-03-13', transaction['day'])
        self.assertEqual('90.00', transaction['wallet']['balance'])

