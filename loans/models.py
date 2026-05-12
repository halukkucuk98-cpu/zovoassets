from django.db import models


class Loan(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="loans")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} — ${self.amount} [{self.status}]"

    class Meta:
        ordering = ["-created_at"]
