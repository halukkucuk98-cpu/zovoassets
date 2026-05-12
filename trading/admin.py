from django.contrib import admin
from .models import Asset, Trade


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("symbol", "name", "asset_type", "current_price", "change_24h_display", "is_active")
    list_editable = ("is_active",)
    list_filter = ("asset_type", "is_active")


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ("user", "asset", "side", "quantity", "entry_price", "status", "pnl", "created_at")
    list_filter = ("status", "side", "asset")
    search_fields = ("user__email", "asset__symbol")
    readonly_fields = ("created_at", "closed_at", "pnl")
