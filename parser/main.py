import django


def main():
    django.setup()

    from app.products.models import ProductPrice, Product
    from parser.price_updater import PriceUpdater
    from parser.price_change_detector import PriceChangeDetector

    updater = PriceUpdater()
    price_change_detector = PriceChangeDetector()
    # new since 11:37 07.06
    while True:
        # time.sleep(10)
        # price_change_detector.detect(Product.objects.order_by('?').first(), 1100)
        for product in Product.objects.order_by('?').iterator(chunk_size=1):
            try:
                name, price = updater.update(product)
                if Product.objects.filter(id=product.id).exists():
                    if name:
                        product.name = name
                        product.save()
                    try:
                        price_change_detector.detect(product, price)
                    except price_change_detector.NoChangesError:
                        pass
                    ProductPrice.objects.create(product=product, price=price)
            except updater.ParseException:
                pass


if __name__ == '__main__':
    main()
