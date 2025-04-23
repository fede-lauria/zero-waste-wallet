from django.db import models

from core.models.users import User




class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallets')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='wallet_currency')


    def __str__(self):
        return f'{self.name} - {self.user.username}'

    def remove_amount(self, amount):
        self.balance -= amount
        self.save()

    def add_amount(self, amount):
        self.balance += amount
        self.save()

