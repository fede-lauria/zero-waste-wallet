from django.test import TestCase

from builder.user_builder import UserBuilder
from builder.wallet_builder import WalletBuilder
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestGetWallet(TestCase):
    def test_return_error_if_user_is_not_logged(self):
        query = '''
                    query {
                          walletsTotalBalance {
                            totalBalance
                            userId
                          }
                    }

                '''

        response = GraphQLClient(schema).execute(query)
        self.assertEqual('User not authorized', response['errors'][0]['message'])

    def test_return_total_balance(self):
        user = UserBuilder().build()
        WalletBuilder().with_name("Wallet di test").with_balance("34.98").with_user(user).build()
        WalletBuilder().with_name("Wallet di test2").with_balance("80.00").with_user(user).build()

        query = '''
            query {
                  walletsTotalBalance {
                    totalBalance
                    userId
                  }
            }

        '''

        response = GraphQLClient(schema).execute(query, user)
        self.assertEqual(user.id, response['data']['walletsTotalBalance']['userId'])
        self.assertEqual(114.98, response['data']['walletsTotalBalance']['totalBalance'])
