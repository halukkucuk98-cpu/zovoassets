from django.urls import path
from . import withdrawal_views as views

urlpatterns = [
    path("", views.withdraw, name="withdraw"),
    path("pin/", views.set_pin, name="set_pin"),
    path("history/", views.withdrawal_history, name="withdrawal_history"),
]
