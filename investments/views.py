from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Investment, InvestmentPlan
from decimal import Decimal


@login_required
def new_investment(request):
    plans = InvestmentPlan.objects.filter(is_active=True)
    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        amount_str = request.POST.get("amount", "0").replace(",", "")
        try:
            plan = InvestmentPlan.objects.get(id=plan_id, is_active=True)
            amount = Decimal(amount_str)
        except (InvestmentPlan.DoesNotExist, Exception):
            messages.error(request, "Invalid plan or amount.")
            return render(request, "investments/new.html", {"plans": plans})

        if amount < plan.min_amount:
            messages.error(request, f"Minimum for {plan.name} is ${plan.min_amount:,.0f}")
            return render(request, "investments/new.html", {"plans": plans})

        Investment.objects.create(user=request.user, plan=plan, amount=amount, status="pending")
        messages.success(request, "Investment submitted! Awaiting admin activation.")
        return redirect("dashboard")

    return render(request, "investments/new.html", {"plans": plans})
