from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("kyc/", views.kyc_submit, name="kyc_submit"),
    path("referral/", views.referral, name="referral"),
]
