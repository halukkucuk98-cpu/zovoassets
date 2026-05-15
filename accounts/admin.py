from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import Profile, KYC, Withdrawal
from core.models import Wallet


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "referral_code", "referral_bonus_earned", "created_at")
    search_fields = ("user__email", "referral_code")


def approve_kyc(modeladmin, request, queryset):
    updated = queryset.filter(status="pending").update(status="approved", reviewed_at=timezone.now())
    messages.success(request, f"{updated} KYC(s) approved.")
approve_kyc.short_description = "Approve selected KYC"

def reject_kyc(modeladmin, request, queryset):
    updated = queryset.filter(status="pending").update(status="rejected", reviewed_at=timezone.now())
    messages.success(request, f"{updated} KYC(s) rejected.")
reject_kyc.short_description = "Reject selected KYC"

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ("user", "id_type", "id_number", "status", "submitted_at", "reviewed_at")
    list_filter = ("status", "id_type")
    actions = [approve_kyc, reject_kyc]
    readonly_fields = ("submitted_at", "reviewed_at")


def complete_withdrawals(modeladmin, request, queryset):
    count = 0
    for w in queryset.filter(status="pending"):
        w.status = "completed"
        w.processed_at = timezone.now()
        w.save()
        count += 1
    messages.success(request, f"{count} withdrawal(s) marked as completed.")
complete_withdrawals.short_description = "Mark as completed"

def reject_withdrawals(modeladmin, request, queryset):
    count = 0
    for w in queryset.filter(status="pending"):
        w.status = "rejected"
        w.processed_at = timezone.now()
        w.save()
        wallet, _ = Wallet.objects.get_or_create(user=w.user)
        wallet.balance += w.amount_usd
        wallet.save()
        count += 1
    messages.success(request, f"{count} withdrawal(s) rejected and funds returned.")
reject_withdrawals.short_description = "Reject & refund balance"

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("user", "coin", "amount_usd", "wallet_address", "status", "created_at", "processed_at")
    list_filter = ("status", "coin")
    search_fields = ("user__email", "wallet_address", "txid")
    actions = [complete_withdrawals, reject_withdrawals]
    readonly_fields = ("created_at", "processed_at")
