from django.contrib import admin
from core.models import Wallet, Transaction, User


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'balance')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet', 'text', 'amount', )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff',
                    'date_joined']