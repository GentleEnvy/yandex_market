from collections import defaultdict
from typing import Any

from app.products.models import Product
from app.users.models import User
from parser.price_change_detector import PriceChangeDetector


class PriceChangeNotifier:
    def __init__(self):
        self.price_change_detector = PriceChangeDetector()
        self.product_manager = Product.objects

    def notify_all(self) -> dict[User, dict[Product, dict[str, Any]]]:
        notifications = defaultdict(dict)
        changes = self.price_change_detector.get()  # FIXME: pop_all
        products = self.product_manager.filter(id__in=changes.keys()).prefetch_related(
            'users'
        )
        for product in products:
            for user in product.users.all():
                notifications[user][product] = changes[product.id]
        return notifications
