from django.core.management.base import BaseCommand
from trading.models import Asset

ASSETS = [
    # Crypto
    {"symbol": "BTC",  "name": "Bitcoin",        "asset_type": "crypto", "base_price": 67500.00,  "color": "#F7931A", "icon_letters": "BTC"},
    {"symbol": "ETH",  "name": "Ethereum",        "asset_type": "crypto", "base_price": 3500.00,   "color": "#627EEA", "icon_letters": "ETH"},
    {"symbol": "BNB",  "name": "BNB",             "asset_type": "crypto", "base_price": 580.00,    "color": "#F3BA2F", "icon_letters": "BNB"},
    {"symbol": "SOL",  "name": "Solana",          "asset_type": "crypto", "base_price": 175.00,    "color": "#9945FF", "icon_letters": "SOL"},
    {"symbol": "XRP",  "name": "Ripple",          "asset_type": "crypto", "base_price": 0.6200,    "color": "#00AAE4", "icon_letters": "XRP"},
    {"symbol": "ADA",  "name": "Cardano",         "asset_type": "crypto", "base_price": 0.4500,    "color": "#0033AD", "icon_letters": "ADA"},
    {"symbol": "DOGE", "name": "Dogecoin",        "asset_type": "crypto", "base_price": 0.1600,    "color": "#C2A633", "icon_letters": "DOGE"},
    {"symbol": "AVAX", "name": "Avalanche",       "asset_type": "crypto", "base_price": 38.00,     "color": "#E84142", "icon_letters": "AVAX"},
    # Stocks
    {"symbol": "AAPL", "name": "Apple Inc.",      "asset_type": "stock",  "base_price": 189.00,    "color": "#555555", "icon_letters": "AAPL"},
    {"symbol": "TSLA", "name": "Tesla Inc.",      "asset_type": "stock",  "base_price": 245.00,    "color": "#CC0000", "icon_letters": "TSLA"},
    {"symbol": "NVDA", "name": "NVIDIA Corp.",    "asset_type": "stock",  "base_price": 875.00,    "color": "#76B900", "icon_letters": "NVDA"},
    {"symbol": "MSFT", "name": "Microsoft Corp.", "asset_type": "stock",  "base_price": 415.00,    "color": "#00A4EF", "icon_letters": "MSFT"},
    {"symbol": "AMZN", "name": "Amazon.com",      "asset_type": "stock",  "base_price": 185.00,    "color": "#FF9900", "icon_letters": "AMZN"},
    {"symbol": "GOOG", "name": "Alphabet Inc.",   "asset_type": "stock",  "base_price": 175.00,    "color": "#4285F4", "icon_letters": "GOOG"},
    {"symbol": "META", "name": "Meta Platforms",  "asset_type": "stock",  "base_price": 500.00,    "color": "#0082FB", "icon_letters": "META"},
]

class Command(BaseCommand):
    help = 'Seed trading assets (crypto + stocks)'

    def handle(self, *args, **kwargs):
        created_count = 0
        updated_count = 0
        for a in ASSETS:
            obj, created = Asset.objects.update_or_create(
                symbol=a['symbol'],
                defaults={**a, 'current_price': a['base_price']}
            )
            if created:
                created_count += 1
                self.stdout.write(f"  Created: {obj}")
            else:
                updated_count += 1
                self.stdout.write(f"  Updated: {obj}")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created_count} created, {updated_count} updated. Total: {Asset.objects.count()} assets.'
        ))