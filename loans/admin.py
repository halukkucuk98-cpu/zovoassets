from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import Loan


def approve_loans(modeladmin, request, queryset):
    updated = queryset.filter(status="pending").update(status="approved", reviewed_at=timezone.now())
    messages.success(request, f"{updated} loan(s) approved.")

approve_loans.short_description = "Approve selected loans"


def reject_loans(modeladmin, request, queryset):
    updated = queryset.filter(status="pending").update(status="rejected", reviewed_at=timezone.now())
    messages.success(request, f"{updated} loan(s) rejected.")

reject_loans.short_description = "Reject selected loans"


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "purpose_short", "status", "created_at", "reviewed_at")
    list_filter = ("status",)
    search_fields = ("user__email",)
    actions = [approve_loans, reject_loans]
    readonly_fields = ("created_at", "reviewed_at")
    fields = ("user", "amount", "purpose", "status", "admin_note", "created_at", "reviewed_at")

    def purpose_short(self, obj):
        return obj.purpose[:60] + "..." if len(obj.purpose) > 60 else obj.purpose
    purpose_short.short_description = "Purpose"
