from django.test import TestCase

from builder.currency_builder import CurrencyBuilder
from builder.user_builder import UserBuilder
from builder.wallet_builder import WalletBuilder
from core.models import Currency
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestCreatePatientAPI(TestCase):

    def test_return_error_if_user_is_not_logged(self):
        query = '''
                    mutation createPatient(
                      $firstName: String!,
                      $lastName: String!,
                      $email: String!,
                      $phone: String!,
                      $dateOfBirth: Date!,
                      $status: Boolean!,
                      $nextAppointment: Date!,
                      $lastAppointment: Date!,
                      $height: Decimal,
                      $weight: Decimal
                    ) {
                      createPatient(
                        input: {
                          firstName: $firstName,
                          lastName: $lastName,
                          email: $email,
                          phone: $phone,
                          dateOfBirth: $dateOfBirth,
                          status: $status,
                          nextAppointment: $nextAppointment,
                          lastAppointment: $lastAppointment,
                          height: $height,
                          weight: $weight
                        }
                      ) {
                        patients { id }
                      }
                    }'''

        response = GraphQLClient(schema).execute(query, variables={
            "firstName": "Antonio",
            "lastName": "Rossi",
            "email": "fede@gmail.com",
            "phone": "3334445556",
            "dateOfBirth": "1990-01-01",
            "status": True,
            "nextAppointment": "2025-03-13",
            "lastAppointment": "2025-03-13",
            "height": "170.00",
            "weight": "70.00"
        })
        self.assertEqual('User not authorized', response['errors'][0]['message'])


    def test_create_wallet(self):
        user = UserBuilder().build()
        query = '''
                            mutation createPatient(
                              $firstName: String!,
                              $lastName: String!,
                              $email: String!,
                              $phone: String!,
                              $dateOfBirth: Date!,
                              $status: Boolean!,
                              $nextAppointment: Date!,
                              $lastAppointment: Date!,
                              $height: Decimal,
                              $weight: Decimal
                            ) {
                              createPatient(
                                input: {
                                  firstName: $firstName,
                                  lastName: $lastName,
                                  email: $email,
                                  phone: $phone,
                                  dateOfBirth: $dateOfBirth,
                                  status: $status,
                                  nextAppointment: $nextAppointment,
                                  lastAppointment: $lastAppointment,
                                  height: $height,
                                  weight: $weight
                                }
                              ) {
                                patients { id, firstName, lastName, email, phone, dateOfBirth, status, nextAppointment, lastAppointment, height, weight }
                              }
                            }'''

        response = GraphQLClient(schema).execute(query, user, variables={
            "firstName": "Antonio",
            "lastName": "Rossi",
            "email": "fede@gmail.com",
            "phone": "3334445556",
            "dateOfBirth": "1990-01-01",
            "status": True,
            "nextAppointment": "2025-03-13",
            "lastAppointment": "2025-03-13",
            "height": "170.00",
            "weight": "70.00"
        })

        self.assertNotIn('errors', response)
        patient = response['data']['createPatient']['patients']
        self.assertEqual('Antonio', patient['firstName'])
        self.assertEqual('Rossi', patient['lastName'])




