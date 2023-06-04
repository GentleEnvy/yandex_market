from app.base.views import BaseView
from app.products.models import ProductPrice
from app.products.serializers.prices import ProductPricesSerializer


class ProductPricesView(BaseView):
    many = True
    serializer_map = {'get': ProductPricesSerializer}

    def get(self):
        return self.list()

    def get_queryset(self):
        id = self.kwargs['id']
        return (
            ProductPrice.objects.filter(product=id, product__name__isnull=False)
            .exclude(product__name='')
            .order_by('-saved_at')
        )
