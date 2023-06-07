import django


def main():
    django.setup()

    from app.products.models import ProductPrice, Product
    from parser.price_updater import PriceUpdater

    i = 0
    updater = PriceUpdater()
    # new since 11:37 07.06
    while True:
        for product in Product.objects.all().iterator(chunk_size=1):
            try:
                name, price = updater.update(product)
                if Product.objects.filter(id=product.id).exists():
                    if name:
                        product.name = name
                        product.save()
                    ProductPrice.objects.create(product=product, price=price)
                print(f"iteration: {i}")  # FIXME: during the tests
                i += 1
            except updater.ParseException:
                pass


if __name__ == '__main__':
    main()
