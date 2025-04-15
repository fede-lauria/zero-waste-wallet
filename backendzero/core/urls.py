from django.urls import path
from .views import protected_view, register

urlpatterns = [
    path('protected/', protected_view),
    path('register/', register),
]
