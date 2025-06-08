from django.db import models
from core.models import User


class Patients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    status = models.BooleanField(default=True)
    next_appointment = models.DateField(blank=True, null=True)
    last_appointment = models.DateField()
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'