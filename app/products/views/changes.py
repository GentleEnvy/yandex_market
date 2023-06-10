from rest_framework.response import Response

from app.base.permissions.superuser import SuperuserPermission
from app.base.views import BaseView
from app.products.serializers.changes import GETProductsChangesSerializer
from app.products.services.price_change_notifier import PriceChangeNotifier


class ProductsChangesView(BaseView):
    serializer_map = {'get': GETProductsChangesSerializer}
    permissions_map = {'get': [SuperuserPermission]}

    def get(self):
        price_change_notifier = PriceChangeNotifier()
        notifications = price_change_notifier.notify_all()
        serializer = self.get_serializer(
            instance=notifications.keys(),
            context=self.get_serializer_context() | {'notifications': notifications},
            many=True,
        )
        return Response(serializer.data)
