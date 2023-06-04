from rest_framework.response import Response

from app.base.views import BaseView
from app.products.models import Product


class ProductView(BaseView):
    queryset = Product.objects.all()

    def get(self):
        product = self.get_object()
        last_price = product.last_price
        return Response(
            data={
                'name': product.name,
                'last_price': last_price.price if last_price else None,
                'saved_at': last_price.saved_at if last_price else None,
            }
        )
