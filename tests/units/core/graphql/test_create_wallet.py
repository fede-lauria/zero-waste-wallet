from django.test import TestCase

from builder.currency_builder import CurrencyBuilder
from builder.user_builder import UserBuilder
from builder.wallet_builder import WalletBuilder
from core.models import Currency
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestCreateMenuAPI(TestCase):

    def test_return_error_if_user_is_not_logged(self):
        query = '''
                    mutation createWallet(
                      $name: String!,
                      $balance: Decimal
                    ) {
                      createWallet(
                        input: {
                          name: $name,
                          balance: $balance
                        }
                      ) {
                        wallet { id, name, balance}
                      }
                    }'''

        response = GraphQLClient(schema).execute(query, variables={
            "name": "Revolut",
            "balance": "1987.98"
        })
        self.assertEqual('User not authorized', response['errors'][0]['message'])


    def test_create_wallet(self):
        user = UserBuilder().build()
        currency = CurrencyBuilder().build()

        query = '''
            mutation createWallet(
              $name: String!,
              $balance: Decimal,
              $currency: ID!
            ) {
              createWallet(
                input: {
                  name: $name,
                  balance: $balance,
                  currency: $currency
                }
              ) {
                wallet { id, name, balance, currency { id, name, symbol } }
              }
            }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "name": "Revolut",
            "balance": "1987.98",
            "currency": currency.id
        })
        self.assertNotIn('errors', response)
        self.assertEqual(response['data']['createWallet']['wallet']['name'], "Revolut")
        self.assertEqual(response['data']['createWallet']['wallet']['balance'], '1987.98')
        self.assertEqual(response['data']['createWallet']['wallet']['currency']['id'], str(currency.id))
        self.assertEqual(response['data']['createWallet']['wallet']['currency']['name'], "EUR")
        self.assertEqual(response['data']['createWallet']['wallet']['currency']['symbol'], "€")




