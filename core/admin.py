from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Wallet


class WalletInline(admin.StackedInline):
    model = Wallet
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "full_name", "phone", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)
    inlines = [WalletInline]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2"),
        }),
    )
    readonly_fields = ("date_joined",)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "total_invested", "total_profit", "updated_at")
    search_fields = ("user__email",)
    readonly_fields = ("created_at", "updated_at")
