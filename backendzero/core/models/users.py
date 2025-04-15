from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    address = models.TextField(verbose_name="Indirizzo")
    phone = models.CharField(max_length=32, verbose_name="Telefono")
