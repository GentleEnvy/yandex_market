from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from app.products.models import Product


class GETProductsSerializer(serializers.ModelSerializer):
    last_price = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'url', 'last_price']

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_last_price(self, obj):
        latest_price = obj.productprice_set.order_by('-saved_at').first()
        return latest_price.price if latest_price else None


class POSTProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'url']
