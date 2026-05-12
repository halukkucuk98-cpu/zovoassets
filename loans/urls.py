from django.urls import path
from . import views

urlpatterns = [
    path("request/", views.request_loan, name="request_loan"),
    path("history/", views.loan_history, name="loan_history"),
]
