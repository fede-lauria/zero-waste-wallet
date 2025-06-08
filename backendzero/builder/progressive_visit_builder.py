from datetime import date

from dateutil.utils import today
from model_bakery import baker

from builder.user_builder import UserBuilder
from core.models import Patients, ProgressiveVisit


class ProgressiveVisitBuilder:
    def __init__(self):
        self.user = None
        self.patient = None
        self.date = today()
        self.next_appointment = date(2025, 7, 10)
        self.visit_type = "Controllo"
        self.pay = False
        self.weight = "88"
        self.BMI = "29"

    def with_user(self, user):
        self.user = user
        return self

    def with_patient(self, patient):
        self.patient = patient
        return self

    def with_date(self, date):
        self.date = date
        return self

    def build(self):
        if self.user is None:
            self.user = UserBuilder().build()
        progressive_visit = baker.make(ProgressiveVisit, user=self.user, patient=self.patient,
                                       date=self.date, next_appointment=self.next_appointment,
                                       visit_type=self.visit_type, pay=self.pay,
                                       weight=self.weight, BMI=self.BMI)

        return progressive_visit

