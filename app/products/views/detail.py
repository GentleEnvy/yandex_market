from rest_framework.response import Response

from app.base.utils.common import response_204
from app.base.views import BaseView
from app.products.models import Product, UserProduct
from app.users.permissions import AuthenticatedPermission


class ProductView(BaseView):
    queryset = Product.objects.all()
    permissions_map = {'delete': [AuthenticatedPermission]}

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

    @response_204
    def delete(self):
        product = self.get_object()
        user = self.request.user
        UserProduct.objects.filter(user=user, product=product).delete()
        if not UserProduct.objects.filter(product=product).exists():
            product.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.method == 'delete':
            return queryset.filter(users=self.request.user)
        return queryset
