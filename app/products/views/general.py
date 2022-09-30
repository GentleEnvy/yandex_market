from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from app.products.models import Product
from app.products.serializers.general import (
    GETProductsSerializer,
    POSTProductsSerializer,
)


class ProductsView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Product.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def get_serializer_class(self):
        match self.request.method.lower():
            case 'get':
                return GETProductsSerializer
            case 'post':
                return POSTProductsSerializer
