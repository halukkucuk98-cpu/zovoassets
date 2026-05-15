import hashlib
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Withdrawal, WithdrawalPin


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


COIN_MINIMUMS = {"BTC": 50, "ETH": 50, "USDT": 50}
COIN_NETWORKS = {"BTC": "Bitcoin Network", "ETH": "ERC20 / TRC20", "USDT": "TRC20 Network"}


@login_required
def set_pin(request):
    has_pin = WithdrawalPin.objects.filter(user=request.user).exists()
    if request.method == "POST":
        pin = request.POST.get("pin", "").strip()
        confirm_pin = request.POST.get("confirm_pin", "").strip()
        if len(pin) != 4 or not pin.isdigit():
            messages.error(request, "PIN must be exactly 4 digits.")
            return render(request, "withdrawals/set_pin.html", {"has_pin": has_pin})
        if pin != confirm_pin:
            messages.error(request, "PINs do not match.")
            return render(request, "withdrawals/set_pin.html", {"has_pin": has_pin})
        WithdrawalPin.objects.update_or_create(
            user=request.user, defaults={"pin_hash": hash_pin(pin)}
        )
        messages.success(request, "Withdrawal PIN set successfully.")
        return redirect("withdraw")
    return render(request, "withdrawals/set_pin.html", {"has_pin": has_pin})


@login_required
def withdraw(request):
    user = request.user
    wallet = user.wallet
    has_pin = WithdrawalPin.objects.filter(user=user).exists()
    if not has_pin:
        messages.info(request, "Please set a withdrawal PIN first.")
        return redirect("set_pin")

    if request.method == "POST":
        coin = request.POST.get("coin", "BTC").upper()
        amount_str = request.POST.get("amount_usd", "0").replace(",", "")
        wallet_address = request.POST.get("wallet_address", "").strip()
        pin = request.POST.get("pin", "").strip()

        try:
            pin_obj = WithdrawalPin.objects.get(user=user)
            if pin_obj.pin_hash != hash_pin(pin):
                messages.error(request, "Incorrect withdrawal PIN.")
                return redirect("withdraw")
        except WithdrawalPin.DoesNotExist:
            messages.error(request, "Please set a withdrawal PIN first.")
            return redirect("set_pin")

        try:
            amount = Decimal(amount_str)
        except InvalidOperation:
            messages.error(request, "Invalid amount.")
            return redirect("withdraw")

        min_amount = COIN_MINIMUMS.get(coin, 50)
        if amount < min_amount:
            messages.error(request, f"Minimum withdrawal for {coin} is ${min_amount}.")
            return redirect("withdraw")

        if amount > wallet.balance:
            messages.error(request, f"Insufficient balance. Available: ${wallet.balance:,.2f}")
            return redirect("withdraw")

        if not wallet_address:
            messages.error(request, "Please enter your wallet address.")
            return redirect("withdraw")

        # Check cooldown
        last = Withdrawal.objects.filter(
            user=user, status__in=["pending", "processing"]
        ).order_by("-created_at").first()
        if last:
            cooldown_end = last.created_at + timedelta(hours=24)
            if timezone.now() < cooldown_end:
                remaining = cooldown_end - timezone.now()
                hours = int(remaining.total_seconds() // 3600)
                minutes = int((remaining.total_seconds() % 3600) // 60)
                messages.error(request, f"You can request another withdrawal in {hours}h {minutes}m.")
                return redirect("withdraw")

        wallet.balance -= amount
        wallet.save()

        Withdrawal.objects.create(
            user=user, coin=coin, amount_usd=amount,
            wallet_address=wallet_address, status="pending",
        )
        messages.success(request, f"Withdrawal of ${amount:,.2f} submitted. Processing within 24 hours.")
        return redirect("withdrawal_history")

    pending_count = Withdrawal.objects.filter(user=user, status="pending").count()
    return render(request, "withdrawals/withdraw.html", {
        "wallet": wallet,
        "pending_count": pending_count,
        "networks": COIN_NETWORKS,
    })


@login_required
def withdrawal_history(request):
    withdrawals = request.user.withdrawal_requests.all()
    return render(request, "withdrawals/history.html", {"withdrawals": withdrawals})
