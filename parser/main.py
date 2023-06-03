import django


def main():
    django.setup()

    from app.products.models import ProductPrice, Product
    from parser.price_updater import PriceUpdater

    i = 0
    updater = PriceUpdater()
    while True:
        for product in Product.objects.all():
            try:
                name, price = updater.update(product)
                if name:
                    product.name = name
                    product.save()
                ProductPrice.objects.create(product=product, price=price)
                print(i)  # FIXME: during the tests
                i += 1
            except updater.ParseException:
                pass


if __name__ == '__main__':
    main()
