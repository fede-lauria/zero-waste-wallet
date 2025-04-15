from django.test import TestCase

from builder.user_builder import UserBuilder
from builder.wallet_builder import WalletBuilder
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestGetWallet(TestCase):
    def test_return_error_if_user_is_not_logged(self):
        query = '''
            query {
                wallets {
                    id
                    name
                    balance
                }
            }
        '''

        response = GraphQLClient(schema).execute(query)
        self.assertEqual('User not authorized', response['errors'][0]['message'])

    def test_return_my_wallets(self):
        user = UserBuilder().build()
        wallet1 = WalletBuilder().with_name("Wallet di test").with_user(user).build()
        wallet2 = WalletBuilder().with_name("Wallet di test2").build()
        query = '''
                    query {
                        wallets {
                            id
                            name
                            balance
                            user{ id }
                        }
                    }
                '''

        response = GraphQLClient(schema).execute(query, user=user)
        print(response)
        self.assertEqual(1, len(response['data']['wallets']))
        user_response = response['data']['wallets'][0]['user']
        self.assertEqual(str(user.id), user_response["id"])

    def test_return_wallet_by_id(self):
        user = UserBuilder().build()
        wallet1 = WalletBuilder().with_name("Wallet di test").with_user(user).build()
        wallet2 = WalletBuilder().with_name("Wallet di test2").with_user(user).build()
        query = '''
                    query wallet($id: Int) {
                      wallet(id: $id) {
                        id
                        name
                        balance
                        user{ id }
                      }
                    }
                '''

        response = GraphQLClient(schema).execute(query, user=user, variables={'id': wallet2.id} )
        self.assertEqual(str(wallet2.id), response['data']['wallet']['id'])
        self.assertEqual("Wallet di test2", response['data']['wallet']['name'])
        user_response = response['data']['wallet']['user']
        self.assertEqual(str(user.id), user_response["id"])


