from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from app.products.models import ProductPrice
from app.products.serializers.prices import ProductPricesSerializer


class ProductPricesView(ListModelMixin, GenericAPIView):
    serializer_class = ProductPricesSerializer

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        id = self.kwargs['id']
        return ProductPrice.objects.filter(
            product=id, product__name__isnull=False
        ).exclude(product__name='').order_by('-saved_at')
