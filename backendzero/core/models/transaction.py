from datetime import datetime

from django.db import models
from django.utils import timezone

from core.models.users import User




class Transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, related_name='wallet_transactions')
    text = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    flow = models.IntegerField(default=1) #1 --> + , 0 --> -
    day = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f'{self.text} - {self.user.username} - {self.amount} '
