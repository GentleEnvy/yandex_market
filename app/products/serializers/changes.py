from typing import Any

from rest_framework import serializers

from app.base.serializers.base import BaseModelSerializer
from app.products.models import Product
from app.users.models import User


class _GETProductsChanges_ChangesSerializer(BaseModelSerializer):
    old_price = serializers.IntegerField()
    new_price = serializers.IntegerField()
    changed_at = serializers.DateTimeField()

    class Meta:
        model = Product
        read_only_fields = ['id', 'name', 'old_price', 'new_price', 'changed_at']


class GETProductsChangesSerializer(BaseModelSerializer):
    changes = _GETProductsChanges_ChangesSerializer(many=True)

    class Meta:
        model = User
        read_only_fields = ['username', 'telegram_id', 'changes']

    def to_representation(self, instance: User):
        notifications: dict[User, dict[Product, dict[str, Any]]] = self.context[
            'notifications'
        ]
        instance.changes = []
        for product, change in notifications[instance].items():
            for key, value in change.items():
                setattr(product, key, value)
            instance.changes.append(product)
        return super().to_representation(instance)
