import io

import matplotlib.pyplot as plt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from app.base.utils.common import create_slug
from app.products.models import Product, ProductPrice


class ProductsPlotView(GenericAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get(self, request, **_):
        content = self.generate_price_plot()
        response = Response(content_type='image/png')
        response[
            'Content-Disposition'
        ] = f'attachment; filename="{create_slug(self.get_object().name)}_plot.png"'
        response.content = content
        return response

    def generate_price_plot(self):
        product = self.get_object()
        prices = ProductPrice.objects.filter(product=product).order_by('saved_at')
        plt.plot(
            [p.saved_at for p in prices],
            [p.price for p in prices],
            linestyle='-',
            label='Price',
        )

        for p in prices:
            plt.scatter(p.saved_at, p.price, color='blue', marker='o', s=3)

        change_indexes = [0]
        stable_price = prices[0].price
        for index in range(1, len(prices) - 1):
            current_price = prices[index].price
            if stable_price != current_price:
                change_indexes.append(index)
                stable_price = current_price
        change_indexes.append(len(prices) - 1)

        for change_index in change_indexes:
            p = prices[change_index]
            plt.scatter(p.saved_at, p.price, color='red', marker='o')
            plt.text(p.saved_at, p.price, str(p.price), ha='center', va='bottom')

        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.title(product.name)
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        return buffer.getvalue()
