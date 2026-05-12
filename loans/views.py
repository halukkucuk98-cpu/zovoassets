from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoanForm
from .models import Loan


@login_required
def request_loan(request):
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.save()
            messages.success(request, "Loan request submitted. We'll review it shortly.")
            return redirect("dashboard")
    else:
        form = LoanForm()
    return render(request, "loans/request.html", {"form": form})


@login_required
def loan_history(request):
    loans = request.user.loans.all()
    return render(request, "loans/history.html", {"loans": loans})
