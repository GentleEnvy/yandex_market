from django.core.cache import cache as django_cache

from app.products.models import Product


class PriceReduceDetector:
    class NoChangesError(Exception):
        pass

    def __init__(self):
        self.cacher = django_cache
        self.cache_prefix = 'price_reduce'

    def detect_reduce(
        self, product: Product, price: int, save: bool = True
    ) -> tuple[int, int]:
        if last_price := product.last_price:
            old_price = last_price.price
            if old_price > price:
                if save:
                    self.set(product.id, old_price, price)
                return old_price, price
            raise self.NoChangesError
        if save:
            self.set(product.id, 0, price)
        return 0, price

    def set(self, product_id: int, old_price: int, new_price: int) -> None:
        self.cacher.set(
            self._cache_key(product_id), (old_price, new_price), timeout=None
        )

    def pop(self, product_id: int) -> tuple[int, int]:
        key = self._cache_key(product_id)
        prices = self.cacher.get(key)
        if not prices:
            raise KeyError
        self.cacher.delete(key)
        return prices

    def _cache_key(self, product_id: int) -> str:
        return f"{self.cache_prefix}:{product_id}"
