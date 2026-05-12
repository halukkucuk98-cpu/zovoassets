from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("investments/", include("investments.urls")),
    path("loans/", include("loans.urls")),
    path("trading/", include("trading.urls")),
]
