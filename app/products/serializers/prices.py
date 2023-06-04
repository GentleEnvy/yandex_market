from app.base.serializers.base import BaseModelSerializer
from app.products.models import ProductPrice


class ProductPricesSerializer(BaseModelSerializer):
    class Meta:
        model = ProductPrice
        read_only_fields = ['id', 'price', 'saved_at']
