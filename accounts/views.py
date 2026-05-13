from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Profile, KYC, Withdrawal, WithdrawalPin


def get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


@login_required
def profile(request):
    prof = get_or_create_profile(request.user)
    kyc = KYC.objects.filter(user=request.user).first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_profile":
            user = request.user
            user.full_name = request.POST.get("full_name", user.full_name).strip()
            user.phone = request.POST.get("phone", user.phone).strip()
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        elif action == "change_password":
            old = request.POST.get("current_password")
            new = request.POST.get("new_password")
            confirm = request.POST.get("confirm_password")
            if not request.user.check_password(old):
                messages.error(request, "Current password is incorrect.")
            elif new != confirm:
                messages.error(request, "New passwords do not match.")
            elif len(new) < 8:
                messages.error(request, "Password must be at least 8 characters.")
            else:
                request.user.set_password(new)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully.")
            return redirect("profile")
    return render(request, "accounts/profile.html", {
        "prof": prof,
        "kyc": kyc,
        "kyc_status": kyc.status if kyc else None,
        "wallet": request.user.wallet,
    })


@login_required
def kyc_submit(request):
    kyc = KYC.objects.filter(user=request.user).first()
    if kyc and kyc.status == "approved":
        messages.info(request, "Your KYC is already approved.")
        return redirect("profile")
    if request.method == "POST":
        id_type = request.POST.get("id_type")
        id_number = request.POST.get("id_number", "").strip()
        if not id_number:
            messages.error(request, "Please enter your ID number.")
            return redirect("kyc_submit")
        kyc_obj, _ = KYC.objects.get_or_create(user=request.user)
        kyc_obj.id_type = id_type
        kyc_obj.id_number = id_number
        kyc_obj.status = "pending"
        if request.FILES.get("id_front"):
            kyc_obj.id_front = request.FILES["id_front"]
        if request.FILES.get("id_back"):
            kyc_obj.id_back = request.FILES["id_back"]
        if request.FILES.get("selfie"):
            kyc_obj.selfie = request.FILES["selfie"]
        kyc_obj.save()
        messages.success(request, "KYC submitted! We will review within 24-48 hours.")
        return redirect("profile")
    return render(request, "accounts/kyc.html", {"kyc": kyc})


@login_required
def referral(request):
    prof = get_or_create_profile(request.user)
    referred_users = request.user.referrals.all()
    referral_url = request.build_absolute_uri(f"/register/?ref={prof.referral_code}")
    return render(request, "accounts/referral.html", {
        "prof": prof,
        "referral_code": prof.referral_code,
        "referral_url": referral_url,
        "referred_users": referred_users,
        "referral_count": referred_users.count(),
        "bonus_earned": prof.referral_bonus_earned,
    })