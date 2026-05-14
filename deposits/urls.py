from django.urls import path
from . import views

urlpatterns = [
    path("", views.deposit, name="deposit"),
    path("history/", views.deposit_history, name="deposit_history"),
]