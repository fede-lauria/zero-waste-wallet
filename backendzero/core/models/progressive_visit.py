from dateutil.utils import today
from django.db import models


class ProgressiveVisit(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_progressive_visits')
    patient = models.ForeignKey('Patients', on_delete=models.CASCADE, related_name='patient_progressive_visits')
    date = models.DateField(default=today())
    next_appointment = models.DateField(blank=True, null=True)
    visit_type = models.CharField(max_length=100)
    pay = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    BMI = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.patient and self.date:
            self.patient.last_appointment = self.date
            self.patient.next_appointment = self.next_appointment
            self.patient.save(update_fields=['last_appointment'])
            self.patient.save(update_fields=['next_appointment'])
