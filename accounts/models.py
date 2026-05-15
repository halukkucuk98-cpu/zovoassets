from django.db import models
import uuid


class Profile(models.Model):
    user = models.OneToOneField("core.User", on_delete=models.CASCADE, related_name="profile")
    avatar_initials = models.CharField(max_length=4, blank=True)
    country = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    referral_code = models.CharField(max_length=12, unique=True, blank=True)
    referred_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals")
    referral_bonus_earned = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} profile"


class KYC(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    ID_TYPES = [
        ("passport", "Passport"),
        ("national_id", "National ID"),
        ("drivers_license", "Driver's License"),
    ]

    user = models.OneToOneField("core.User", on_delete=models.CASCADE, related_name="kyc")
    id_type = models.CharField(max_length=20, choices=ID_TYPES)
    id_number = models.CharField(max_length=50)
    id_front = models.ImageField(upload_to="kyc/", blank=True)
    id_back = models.ImageField(upload_to="kyc/", blank=True)
    selfie = models.ImageField(upload_to="kyc/", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} KYC [{self.status}]"


class Withdrawal(models.Model):
    COIN_CHOICES = [
        ("BTC", "Bitcoin (BTC)"),
        ("ETH", "Ethereum (ETH)"),
        ("USDT", "Tether USDT TRC20"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="withdrawal_requests")
    coin = models.CharField(max_length=10, choices=COIN_CHOICES)
    amount_usd = models.DecimalField(max_digits=14, decimal_places=2)
    wallet_address = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True)
    txid = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} — {self.coin} ${self.amount_usd} [{self.status}]"

    class Meta:
        ordering = ["-created_at"]


class WithdrawalPin(models.Model):
    user = models.OneToOneField("core.User", on_delete=models.CASCADE, related_name="withdrawal_pin")
    pin_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} — PIN set"
