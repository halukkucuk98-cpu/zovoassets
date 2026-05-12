from django import forms
from .models import Loan


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["amount", "purpose"]
        widgets = {
            "amount": forms.NumberInput(attrs={"placeholder": "5000", "min": "100"}),
            "purpose": forms.Textarea(attrs={"placeholder": "Describe the purpose of this loan...", "rows": 4}),
        }
