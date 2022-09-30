from rest_framework import serializers

from app.products.models import Product


class GETProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'url']


class POSTProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'url']
