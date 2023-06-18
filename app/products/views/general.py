from rest_framework.response import Response

from app.base.views import BaseView
from app.products.models import Product
from app.products.serializers.general import (
    GETProductsSerializer,
    POSTProductsSerializer,
)
from app.users.permissions import AuthenticatedPermission


class ProductsView(BaseView):
    many = True
    queryset = Product.objects.all()
    serializer_map = {'get': GETProductsSerializer, 'post': POSTProductsSerializer}
    permissions_map = {'post': [AuthenticatedPermission]}

    def get(self):
        return self.list()

    def post(self):
        serializer = self.get_valid_serializer()
        product = serializer.save()
        self.request.user.products.add(product)
        return Response(serializer.data, status=201)

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user)
