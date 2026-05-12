from django.db import models
from django.utils import timezone
from datetime import timedelta


class InvestmentPlan(models.Model):
    name = models.CharField(max_length=100)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    roi_percent = models.DecimalField(max_digits=5, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.roi_percent}% / {self.duration_days}d)"

    @property
    def display_min(self):
        return f"${self.min_amount:,.0f}"

    @property
    def display_max(self):
        return f"${self.max_amount:,.0f}" if self.max_amount else "No limit"


class Investment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="investments")
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    profit = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.email} — {self.plan.name} ${self.amount}"

    def calculate_profit(self):
        return self.amount * self.plan.roi_percent / 100

    def activate(self):
        self.status = "active"
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        self.profit = self.calculate_profit()
        self.save()
        wallet = self.user.wallet
        wallet.total_invested += self.amount
        wallet.save()

    def complete(self):
        self.status = "completed"
        self.save()
        wallet = self.user.wallet
        wallet.balance += self.amount + self.profit
        wallet.total_profit += self.profit
        wallet.save()

    @property
    def days_remaining(self):
        if self.end_date and self.status == "active":
            delta = self.end_date - timezone.now()
            return max(0, delta.days)
        return None

    @property
    def progress_percent(self):
        if self.start_date and self.end_date and self.status == "active":
            total = (self.end_date - self.start_date).total_seconds()
            elapsed = (timezone.now() - self.start_date).total_seconds()
            return min(100, int((elapsed / total) * 100))
        return 0
