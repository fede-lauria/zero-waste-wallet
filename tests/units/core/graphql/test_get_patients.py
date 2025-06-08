from django.test import TestCase

from builder.patients_builder import PatientsBuilder
from builder.user_builder import UserBuilder
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestGetPatients(TestCase):
    def test_return_error_user_is_not_logged(self):
        patient = PatientsBuilder().build()
        query = '''
                query {
                      patients {
                        id,
                        firstName,
                        lastName,
                        email,
                        phone,
                        dateOfBirth,
                        status,
                        nextAppointment,
                        lastAppointment
                        
                      }
                }
                '''

        response = GraphQLClient(schema).execute(query)
        self.assertEqual('User not authorized', response['errors'][0]['message'])

    def test_get_all_patients(self):
        user = UserBuilder().build()
        patient1 = PatientsBuilder().build()
        patient2 = PatientsBuilder().build()
        query = '''
                query {
                      patients {
                        id,
                        firstName,
                        lastName,
                        email,
                        phone,
                        dateOfBirth,
                        status,
                        nextAppointment,
                        lastAppointment

                      }
                }
                '''

        response = GraphQLClient(schema).execute(query, user)
        self.assertNotIn('errors', response)
        self.assertEqual(2, len(response['data']['patients']))

    def test_get_my_patients(self):
        user = UserBuilder().build()
        patient1 = PatientsBuilder().with_user(user).build()
        patient2 = PatientsBuilder().build()
        query = '''
                query {
                      patients {
                        id,
                        firstName,
                        lastName,
                        email,
                        phone,
                        dateOfBirth,
                        status,
                        nextAppointment,
                        lastAppointment
                      }
                }
                '''

        response = GraphQLClient(schema).execute(query, user)
        self.assertNotIn('errors', response)
        self.assertEqual(1, len(response['data']['patients']))
