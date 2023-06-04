from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from app.base.serializers.base import BaseModelSerializer
from app.products.models import Product


class GETProductsSerializer(BaseModelSerializer):
    last_price = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Product
        read_only_fields = ['id', 'name', 'url', 'last_price']

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_last_price(self, obj):
        last_price = obj.last_price
        return last_price.price if last_price else None


class POSTProductsSerializer(BaseModelSerializer):
    class Meta:
        model = Product
        write_only_fields = ['url']
        read_only_fields = ['id']

    def to_internal_value(self, data):
        data['url'] = Product.normalize_url(data['url'])
        return super().to_internal_value(data)
