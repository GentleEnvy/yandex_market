from datetime import datetime
from typing import Any

from django.core.cache import cache as django_cache

from app.products.models import Product


class PriceChangeDetector:
    class NoChangesError(Exception):
        pass

    def __init__(self):
        self.cacher = django_cache
        self.cache_key = 'price_changes'

    def detect(
        self,
        product: Product,
        price: int,
        save: bool = True,
        changed_at: datetime = None,
    ) -> tuple[int, int]:
        if last_price := product.last_price:
            old_price = last_price.price
            if old_price != price:
                if save:
                    self.set(product.id, old_price, price, changed_at)
                return old_price, price
            raise self.NoChangesError
        if save:
            self.set(product.id, 0, price, changed_at)
        return 0, price

    def get(self) -> dict[int, dict[str, Any]]:
        return self.cacher.get(self.cache_key, default={})

    def set(
        self,
        product_id: int,
        old_price: int,
        new_price: int,
        changed_at: datetime = None,
    ) -> None:
        changes = self.get()
        changes[product_id] = {
            'old_price': old_price,
            'new_price': new_price,
            'changed_at': changed_at or datetime.now(),
        }
        self.cacher.set(self.cache_key, changes, timeout=24 * 60 * 60)

    def pop(self, product_id: int) -> dict[str, Any]:
        changes = self.get()
        price_info = changes.pop(product_id)
        self.cacher.set(self.cache_key, changes)
        return price_info

    def pop_all(self) -> dict[int, dict[str, Any]]:
        changes = self.get()
        self.cacher.set(self.cache_key, {})
        return changes
