from django.test import TestCase

from builder.user_builder import UserBuilder
from builder.wallet_builder import WalletBuilder
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

        response = GraphQLClient(schema).execute(query, user, variables={
            "name": "Revolut",
            "balance": "1987.98"
        })
        self.assertNotIn('errors', response)
        self.assertEqual(response['data']['createWallet']['wallet']['name'], "Revolut")
        self.assertEqual(response['data']['createWallet']['wallet']['balance'], '1987.98')




