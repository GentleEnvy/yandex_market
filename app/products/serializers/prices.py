from rest_framework import serializers

from app.products.models import ProductPrice


class ProductPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['id', 'price', 'saved_at']
