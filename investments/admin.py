from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import InvestmentPlan, Investment


@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "min_amount", "max_amount", "roi_percent", "duration_days", "is_active")
    list_editable = ("is_active",)


def activate_investments(modeladmin, request, queryset):
    count = 0
    for inv in queryset.filter(status="pending"):
        inv.activate()
        count += 1
    messages.success(request, f"{count} investment(s) activated.")

activate_investments.short_description = "Activate selected investments"


def complete_investments(modeladmin, request, queryset):
    count = 0
    for inv in queryset.filter(status="active"):
        inv.complete()
        count += 1
    messages.success(request, f"{count} investment(s) completed & profit credited.")

complete_investments.short_description = "Complete selected investments (credit ROI)"


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "amount", "profit", "status", "start_date", "end_date", "created_at")
    list_filter = ("status", "plan")
    search_fields = ("user__email", "plan__name")
    actions = [activate_investments, complete_investments]
    readonly_fields = ("profit", "created_at", "start_date", "end_date")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "plan")
