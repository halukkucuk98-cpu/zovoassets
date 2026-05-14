from django.core.management.base import BaseCommand
from investments.models import InvestmentPlan
from trading.models import Asset


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not InvestmentPlan.objects.exists():
            InvestmentPlan.objects.bulk_create([
                InvestmentPlan(name="Starter", min_amount=50, max_amount=499, roi_percent=5, duration_days=7),
                InvestmentPlan(name="Growth", min_amount=500, max_amount=4999, roi_percent=10, duration_days=14),
                InvestmentPlan(name="Premium", min_amount=5000, max_amount=19999, roi_percent=15, duration_days=21),
                InvestmentPlan(name="VIP", min_amount=20000, max_amount=None, roi_percent=20, duration_days=30),
            ])
            self.stdout.write("Investment plans seeded")

        if not Asset.objects.exists():
            assets = [
                ('BTC','Bitcoin','crypto',67240,'#F7931A','BTC'),
                ('ETH','Ethereum','crypto',3480,'#627EEA','ETH'),
                ('BNB','BNB Chain','crypto',412,'#F3BA2F','BNB'),
                ('SOL','Solana','crypto',178,'#9945FF','SOL'),
                ('XRP','Ripple','crypto',0.62,'#00AAE4','XRP'),
                ('ADA','Cardano','crypto',0.58,'#0033AD','ADA'),
                ('AAPL','Apple Inc.','stock',189.5,'#A2AAAD','AAPL'),
                ('TSLA','Tesla Inc.','stock',245.3,'#CC0000','TSLA'),
                ('NVDA','NVIDIA Corp.','stock',875.2,'#76B900','NVDA'),
                ('GOOGL','Alphabet Inc.','stock',175.8,'#4285F4','GOOG'),
                ('AMZN','Amazon.com','stock',198.4,'#FF9900','AMZN'),
                ('MSFT','Microsoft Corp.','stock',420.1,'#00A4EF','MSFT'),
            ]
            for sym,name,atype,base,color,icon in assets:
                Asset.objects.get_or_create(
                    symbol=sym,
                    defaults=dict(name=name,asset_type=atype,base_price=base,current_price=base,color=color,icon_letters=icon)
                )
            self.stdout.write("Assets seeded")

        self.stdout.write("Setup complete")