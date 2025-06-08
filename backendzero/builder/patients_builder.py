from datetime import date

from model_bakery import baker

from builder.user_builder import UserBuilder
from core.models import Patients


class PatientsBuilder:
    def __init__(self):
        self.first_name = 'Andrea'
        self.last_name = 'Pirlo'
        self.email = 'andreapirlo@gmail.com'
        self.phone = '3374896678'
        self.date_of_birth = date(1976, 5, 10)
        self.status = True
        self.next_appointment = date(2025, 7, 10)
        self.last_appointment = date.today()
        self.user = None
        self.height = 175
        self.weight = 88.00

    def with_user(self, user):
        self.user = user
        return self

    def with_height(self, height):
        self.height = height
        return self

    def with_weight(self, weight):
        self.weight = weight
        return self

    def build(self):
        if self.user is None:
            self.user = UserBuilder().build()
        patients = baker.make(Patients, first_name=self.first_name, last_name=self.last_name, email=self.email, phone=self.phone, date_of_birth=self.date_of_birth,
                            status=self.status, user=self.user, last_appointment=self.last_appointment, next_appointment=self.next_appointment, height=self.height, weight=self.weight)
        return patients

