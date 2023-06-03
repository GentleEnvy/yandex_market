from __future__ import annotations

from django.db import models

from app.base.models.base import BaseModel


class Product(BaseModel):
    url = models.URLField(unique=True, max_length=2000)
    name = models.TextField(blank=True, null=True)

    @property
    def last_price(self) -> ProductPrice | None:
        return self.productprice_set.order_by('-saved_at').first()


class ProductPrice(BaseModel):
    product = models.ForeignKey(Product, models.CASCADE)
    price = models.IntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)
