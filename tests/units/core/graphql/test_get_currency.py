from django.test import TestCase

from builder.currency_builder import CurrencyBuilder
from builder.user_builder import UserBuilder
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestGetWallet(TestCase):
    def test_return_error_if_user_is_not_logged(self):
        query = '''
                    query {
                          currency {
                            id,
                            name,
                            symbol
                          }
                    }

                '''

        response = GraphQLClient(schema).execute(query)
        self.assertEqual('User not authorized', response['errors'][0]['message'])

    def test_return_all_currency(self):
        user = UserBuilder().build()
        euro = CurrencyBuilder().with_name('EUR').with_symbol('€').build()
        dollaro = CurrencyBuilder().with_name('USD').with_symbol('$').build()

        query = '''
                    query {
                          currency {
                            id,
                            name,
                            symbol
                          }
                    }

                '''

        response = GraphQLClient(schema).execute(query, user)
        self.assertNotIn('errors', response)
        currency1 = response['data']['currency'][0]
        self.assertEqual(str(euro.id), currency1['id'])
        self.assertEqual('EUR', currency1['name'])
        self.assertEqual('€', currency1['symbol'])
        currency2 = response['data']['currency'][1]
        self.assertEqual(str(dollaro.id), currency2['id'])
        self.assertEqual('USD', currency2['name'])
        self.assertEqual('$', currency2['symbol'])
