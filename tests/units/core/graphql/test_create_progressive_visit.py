from django.test import TestCase

from builder.currency_builder import CurrencyBuilder
from builder.patients_builder import PatientsBuilder
from builder.user_builder import UserBuilder
from builder.wallet_builder import WalletBuilder
from core.models import Currency
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestCreatePatientAPI(TestCase):

    def test_return_error_if_user_is_not_logged(self):
        query = '''
                    mutation createProgressiveVisit(
                      $patient: ID!
                      $weight: Decimal!
                      $date: Date!
                      $visitType: String!
                      $pay: Boolean!
                    ) {
                      createProgressiveVisit(
                        input: {
                          patient: $patient,
                          weight: $weight,
                          date: $date,
                          visitType: $visitType,
                          pay: $pay
                        }
                      ) {
                        progressiveVisit { id }
                      }
                    }'''

        response = GraphQLClient(schema).execute(query, variables={
            "patient": "1",
            "weight": "70.00",
            "date": "2025-03-13",
            "visitType": "Controllo",
            "pay": True,
        })
        self.assertEqual('User not authorized', response['errors'][0]['message'])


    def test_create_progressive_visit(self):
        user = UserBuilder().build()
        patient = PatientsBuilder().build()
        patient_2 = PatientsBuilder().build()
        query = '''
                            mutation createProgressiveVisit(
                              $patient: ID!
                              $weight: Decimal!
                              $date: Date!
                              $visitType: String!
                              $pay: Boolean!
                            ) {
                              createProgressiveVisit(
                                input: {
                                  patient: $patient,
                                  weight: $weight,
                                  date: $date,
                                  visitType: $visitType,
                                  pay: $pay
                                }
                              ) {
                                progressiveVisit { id }
                              }
                            }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "patient": patient.id,
            "weight": "70.00",
            "date": "2025-03-13",
            "visitType": "Controllo",
            "pay": True,
        })

        self.assertNotIn('errors', response)
        self.assertEqual(response['data']['createProgressiveVisit']['progressiveVisit']['id'], '1')

    def test_get_bmi(self):
        user = UserBuilder().build()
        patient = PatientsBuilder().with_height(173).with_user(user).build()
        query = '''
                    mutation getBmi(
                      $patient: ID!,
                      $weight: Float!,
                    ) {
                      getBmi(
                          patient: $patient,
                          weight: $weight
                      ) {
                        bmi
                      }
                    }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "patient": patient.id,
            "weight": 88,
        })
        self.assertNotIn('errors', response)
        self.assertEqual(response['data']['getBmi']['bmi'], 29.4)




