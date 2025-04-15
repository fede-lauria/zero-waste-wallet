from django.test import TestCase

from builder.transaction_builder import TransactionBuilder
from builder.user_builder import UserBuilder
from builder.wallet_builder import WalletBuilder
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestGetTransaction(TestCase):
    def test_return_error_if_user_is_not_logged(self):
        query = '''
            query {
                transactions {
                    id
                    text
                    amount
                }
            }
        '''

        response = GraphQLClient(schema).execute(query)
        self.assertEqual('User not authorized', response['errors'][0]['message'])

    def test_return_my_transactions(self):
        user = UserBuilder().build()
        wallet1 = WalletBuilder().with_name("Wallet di test").with_user(user).build()
        transaction1 = TransactionBuilder().with_user(user).with_amount(100).with_wallet(wallet1).build()
        query = '''
                    query {
                        transactions {
                            id
                            text
                            amount
                            wallet {id, name}
                        }
                    }
                '''

        response = GraphQLClient(schema).execute(query, user=user)
        self.assertEqual(1, len(response['data']['transactions']))
        wallet_response = response['data']['transactions'][0]['wallet']
        self.assertEqual(str(wallet1.id), wallet_response["id"])
        self.assertEqual(wallet1.name, wallet_response["name"])

    def test_return_transaction_by_id(self):
        user = UserBuilder().build()
        wallet = WalletBuilder().with_name("Wallet di test").with_user(user).build()
        transaction = TransactionBuilder().with_user(user).with_amount(100.00).with_wallet(wallet).build()
        query = '''
                    query transaction($id: Int) {
                      transaction(id: $id) {
                        id
                        text
                        amount
                        wallet {id, name}
                      }
                    }
                '''

        response = GraphQLClient(schema).execute(query, user=user, variables={'id': transaction.id} )
        self.assertEqual(str(transaction.id), response['data']['transaction']['id'])
        self.assertEqual(transaction.text, response['data']['transaction']['text'])
        wallet_response = response['data']['transaction']['wallet']
        self.assertEqual(str(wallet.id), wallet_response["id"])
        self.assertEqual(wallet.name, wallet_response["name"])

    def test_return_transactions_by_wallet_id(self):
        user = UserBuilder().build()
        wallet = WalletBuilder().with_name("Wallet di test").with_user(user).with_balance(100.00).build()
        wallet2 = WalletBuilder().with_name("Wallet di test").with_user(user).build()
        balance_wallet_after_transaction = wallet.balance
        transaction1 = TransactionBuilder().with_text("Pizza con gli amici").with_user(user).with_amount(10).with_wallet(wallet).build()
        transaction2 = TransactionBuilder().with_text("Barbiere").with_user(user).with_amount(10).with_wallet(wallet).build()
        transaction3 = TransactionBuilder().with_text("Cochina").with_user(user).with_amount(10).with_wallet(wallet2).build()

        query = '''
                    query transactionsByWallet($id: Int) {
                      transactionsByWallet(id: $id) {
                        id
                        text
                        amount
                        wallet {id, name, balance}
                      }
                    }
                '''

        response = GraphQLClient(schema).execute(query, user=user, variables={'id': wallet.id})
        self.assertEqual(2, len(response['data']['transactionsByWallet']))
        self.assertEqual("Pizza con gli amici", response['data']['transactionsByWallet'][0]['text'])
        self.assertEqual("Barbiere", response['data']['transactionsByWallet'][1]['text'])
        balance = response['data']['transactionsByWallet'][0]['wallet']['balance']




