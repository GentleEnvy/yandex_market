from django.db import models

from app.base.models.base import BaseModel


class Product(BaseModel):
    url = models.URLField(unique=True)
    name = models.TextField(blank=True, null=True)
    
    @property
    def last_price(self) -> int | None:
        product_price = ProductPrice.objects.order_by('-saved_at').first()
        if product_price:
            return product_price.price
        return None


class ProductPrice(BaseModel):
    product = models.ForeignKey(Product, models.CASCADE)
    price = models.IntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)
