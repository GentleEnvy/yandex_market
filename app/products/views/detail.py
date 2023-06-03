from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from app.products.models import ProductPrice, Product
from app.products.services.product_parser import ProductParser


class ProductView(ListModelMixin, GenericAPIView):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        i = 0
        product_parser = ProductParser()
        while True:
            for p in Product.objects.all():
                try:
                    name, price = product_parser.parse(p)
                    if name:
                        p.name = name
                        p.save()
                    ProductPrice.objects.create(product=p, price=price)
                    print(i)
                    i += 1
                except product_parser.ParseException:
                    pass
        product_price = ProductPrice.objects.filter(product=product).last()
        return Response(
            data={
                'name': product.name,
                'last_price': product_price.price if product_price else None,
                'saved_at': product_price.saved_at if product_price else None,
            }
        )
