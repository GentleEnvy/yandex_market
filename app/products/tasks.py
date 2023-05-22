from celery import shared_task

from app.products.models import Product


@shared_task
def update_prices():
    pass
