from django.db import models


class DepositRequest(models.Model):
    COIN_CHOICES = [
        ("BTC", "Bitcoin (BTC)"),
        ("ETH", "Ethereum (ETH)"),
        ("USDT", "Tether (USDT TRC20)"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="deposits")
    coin = models.CharField(max_length=10, choices=COIN_CHOICES)
    amount_usd = models.DecimalField(max_digits=14, decimal_places=2)
    txid = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} — {self.coin} ${self.amount_usd} [{self.status}]"

    class Meta:
        ordering = ["-created_at"]