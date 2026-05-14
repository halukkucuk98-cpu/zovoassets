from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DepositRequest

WALLET_ADDRESSES = {
    "BTC":  "3MGNTKRzvpZ1N1P5mqXCYf7b7gfun8odsX",
    "ETH":  "0x15328BFd7304a9b9423A7f3161e164D1fFEc5e5b",
    "USDT": "TC275hE8BsjrCrAWpm6waiGpmYu24SqRAX",
}

COIN_NETWORKS = {
    "BTC":  "Bitcoin Network",
    "ETH":  "ERC20 / TRC20",
    "USDT": "TRC20 Network",
}

COIN_COLORS = {
    "BTC": "#F7931A",
    "ETH": "#627EEA",
    "USDT": "#26A17B",
}

MIN_DEPOSIT = 50


@login_required
def deposit(request):
    selected_coin = request.GET.get("coin", "BTC").upper()
    if selected_coin not in WALLET_ADDRESSES:
        selected_coin = "BTC"

    if request.method == "POST":
        coin = request.POST.get("coin", "BTC").upper()
        txid = request.POST.get("txid", "").strip()
        amount_str = request.POST.get("amount_usd", "0").replace(",", "")

        try:
            amount = float(amount_str)
        except ValueError:
            messages.error(request, "Enter a valid amount.")
            return redirect("deposit")

        if amount < MIN_DEPOSIT:
            messages.error(request, f"Minimum deposit is ${MIN_DEPOSIT}.")
            return redirect("deposit")

        if not txid:
            messages.error(request, "Please enter your transaction ID.")
            return redirect("deposit")

        DepositRequest.objects.create(
            user=request.user,
            coin=coin,
            amount_usd=amount,
            txid=txid,
            status="pending",
        )
        messages.success(request, "Deposit submitted! We will confirm within 30 minutes.")
        return redirect("deposit_history")

    return render(request, "deposits/deposit.html", {
        "wallet_addresses": WALLET_ADDRESSES,
        "coin_networks": COIN_NETWORKS,
        "coin_colors": COIN_COLORS,
        "selected_coin": selected_coin,
        "min_deposit": MIN_DEPOSIT,
        "coins": WALLET_ADDRESSES.keys(),
    })


@login_required
def deposit_history(request):
    deposits = request.user.deposits.all()
    return render(request, "deposits/history.html", {"deposits": deposits})