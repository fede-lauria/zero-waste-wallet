from django.test import TestCase

from builder.patients_builder import PatientsBuilder
from builder.progressive_visit_builder import ProgressiveVisitBuilder
from builder.user_builder import UserBuilder
from core.schema import schema
from tests.units.graph_ql_client import GraphQLClient


class TestGetProgressiveVisit(TestCase):
    def test_return_wallet_by_id(self):
        user = UserBuilder().build()
        patient = PatientsBuilder().with_user(user).build()
        progressive_visit_1 = ProgressiveVisitBuilder().with_user(user).with_patient(patient).build()
        progressive_visit_2 = ProgressiveVisitBuilder().with_user(user).with_patient(patient).build()

        query = '''
                    query progressiveVisitByPatient($id: Int) {
                      progressiveVisitByPatient(id: $id) {
                        user { id }
                        patient { id }
                        date
                        nextAppointment
                        visitType
                        pay
                        weight
                        BMI
                      }
                    }
                '''

        response = GraphQLClient(schema).execute(query, user=user, variables={'id': patient.id})
        self.assertNotIn('errors', response)