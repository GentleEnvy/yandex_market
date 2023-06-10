import django

from parser.price_reduce_detector import PriceReduceDetector


def main():
    django.setup()

    from app.products.models import ProductPrice, Product
    from parser.price_updater import PriceUpdater

    updater = PriceUpdater()
    price_reduce_detector = PriceReduceDetector()
    # new since 11:37 07.06
    while True:
        for product in Product.objects.all().iterator(chunk_size=1):
            try:
                name, price = updater.update(product)
                if Product.objects.filter(id=product.id).exists():
                    if name:
                        product.name = name
                        product.save()
                    try:
                        old, new = price_reduce_detector.detect_reduce(product, price)
                        print(f"{product.name}: {old, new}")  # FIXME: for test
                    except price_reduce_detector.NoChangesError:
                        print(f"{product.name}: no changes")  # FIXME: for test
                    ProductPrice.objects.create(product=product, price=price)
            except updater.ParseException:
                pass


if __name__ == '__main__':
    main()
