from django.db import models
from django.utils import timezone
import random


class Asset(models.Model):
    ASSET_TYPES = [("crypto", "Crypto"), ("stock", "Stock")]
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES)
    base_price = models.DecimalField(max_digits=16, decimal_places=4)
    current_price = models.DecimalField(max_digits=16, decimal_places=4)
    color = models.CharField(max_length=10, default="#C9A84C")
    icon_letters = models.CharField(max_length=4, default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.symbol} — ${self.current_price}"

    @property
    def change_24h(self):
        if self.base_price:
            return float((self.current_price - self.base_price) / self.base_price * 100)
        return 0

    @property
    def change_24h_display(self):
        c = self.change_24h
        return f"+{c:.2f}%" if c >= 0 else f"{c:.2f}%"

    class Meta:
        ordering = ["asset_type", "symbol"]


class Trade(models.Model):
    SIDE_CHOICES = [("buy", "Buy"), ("sell", "Sell")]
    STATUS_CHOICES = [("open", "Open"), ("closed", "Closed")]

    user = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="trades")
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    side = models.CharField(max_length=4, choices=SIDE_CHOICES)
    quantity = models.DecimalField(max_digits=16, decimal_places=6)
    entry_price = models.DecimalField(max_digits=16, decimal_places=4)
    exit_price = models.DecimalField(max_digits=16, decimal_places=4, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")
    pnl = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} {self.side} {self.quantity} {self.asset.symbol}"

    @property
    def cost_basis(self):
        return float(self.quantity) * float(self.entry_price)

    @property
    def current_value(self):
        return float(self.quantity) * float(self.asset.current_price)

    @property
    def unrealized_pnl(self):
        return self.current_value - self.cost_basis

    @property
    def unrealized_pnl_pct(self):
        cb = self.cost_basis
        return (self.unrealized_pnl / cb * 100) if cb else 0

    def close_position(self):
        self.exit_price = self.asset.current_price
        self.pnl = self.unrealized_pnl
        self.status = "closed"
        self.closed_at = timezone.now()
        self.save()
        wallet = self.user.wallet
        wallet.balance += self.current_value
        wallet.save()
        return self

    class Meta:
        ordering = ["-created_at"]
