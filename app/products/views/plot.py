import io
from textwrap import wrap
from datetime import datetime

import matplotlib.pyplot as plt
from rest_framework.response import Response

from app.base.utils.common import create_slug
from app.base.views import BaseView
from app.products.models import Product, ProductPrice


class ProductsPlotView(BaseView):
    queryset = Product.objects.all()

    def get(self):
        content = self.generate_price_plot()
        response = Response(content_type='image/png')
        response[
            'Content-Disposition'
        ] = f'attachment; filename="{create_slug(self.get_object().name)}_plot.png"'
        response.content = content
        return response

    def generate_price_plot(self):
        product = self.get_object()
        prices = ProductPrice.objects.filter(
            product=product, saved_at__gt=datetime(2023, 6, 7, 11, 37)  # FIXME
        ).order_by('saved_at')
        plt.plot(
            [p.saved_at for p in prices],
            [p.price for p in prices],
            linestyle='-',
            label="Цена",
        )

        dates = [p.saved_at for p in prices]
        prices_list = [p.price for p in prices]
        date_range = max(dates) - min(dates)
        padding = date_range * 0.02
        plt.scatter(dates, prices_list, color='blue', marker='o', s=3)
        plt.xlim(min(dates) - padding, datetime.now() + padding)

        change_indexes = [0]
        stable_price = prices[0].price
        for index in range(1, len(prices) - 1):
            current_price = prices[index].price
            if stable_price != current_price:
                change_indexes.append(index)
                stable_price = current_price
        change_indexes.append(len(prices) - 1)

        showed = set()
        for change_index in change_indexes:
            p = prices[change_index]
            price = p.price
            plt.scatter(p.saved_at, p.price, color='red', marker='o')
            plt.text(
                p.saved_at,
                p.price * 1.003,
                '' if price in showed else str(price),
                ha='center',
                va='bottom',
                fontdict={'size': 9},
                color='darkred',
            )
            showed.add(price)

        plt.xlabel("Время")
        plt.ylabel("Цена")
        plt.title('\n'.join(wrap(product.name, 60)))
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        return buffer.getvalue()
