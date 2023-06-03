from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from app.products.models import Product


class ProductView(ListModelMixin, GenericAPIView):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        last_price = product.last_price
        return Response(
            data={
                'name': product.name,
                'last_price': last_price.price if last_price else None,
                'saved_at': last_price.saved_at if last_price else None,
            }
        )
