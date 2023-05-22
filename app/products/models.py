from django.db import models

from app.base.models.base import BaseModel


class Product(BaseModel):
    url = models.URLField(unique=True, max_length=2000)
    name = models.TextField(blank=True, null=True)


class ProductPrice(BaseModel):
    product = models.ForeignKey(Product, models.CASCADE)
    price = models.IntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)
