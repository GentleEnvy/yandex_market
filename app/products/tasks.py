from celery import shared_task

from app.products.models import Product
from app.products.product_parser import ProductParser


@shared_task
def update_prices():
    parser = ProductParser()
    for product in Product.objects.all():
        parser.parse(product)
