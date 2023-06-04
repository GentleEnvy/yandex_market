from __future__ import annotations

from urllib.parse import urlparse, parse_qs

from django.db import models

from app.base.models.base import BaseModel


class Product(BaseModel):
    url = models.URLField(unique=True, max_length=2000)
    name = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(
        'users.User', through='UserProduct', related_name='products'
    )

    @property
    def last_price(self) -> ProductPrice | None:
        return self.productprice_set.order_by('-saved_at').first()

    @staticmethod
    def normalize_url(url: str) -> str:
        parsed = urlparse(url)
        base_url = f"https://{parsed.netloc}{parsed.path.rstrip('/')}"
        params = parse_qs(parsed.query)
        sku = params.get('sku', [None])[0]
        if sku and sku.isdigit():
            return f"{base_url}?sku={sku}"
        return base_url

    def save(self, **kwargs):
        self.url = self.normalize_url(self.url)
        super().save(**kwargs)


class UserProduct(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductPrice(BaseModel):
    product = models.ForeignKey(Product, models.CASCADE)
    price = models.IntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)
