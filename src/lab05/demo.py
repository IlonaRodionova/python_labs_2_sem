from lab03.base import Product
from lab03.models import Perfume, Skincare, Makeup
from lab05.collection import ProductCatalog
from lab05.strategies import (
    by_name, by_price, by_category_then_price,
    is_available, has_discount, is_perfume,
    make_price_filter, DiscountStrategy, StatusReportStrategy
)


def print_catalog(catalog: ProductCatalog):
    for i, item in enumerate(catalog):
        try:
            price = item.calculate_price()
            print(f"  {i+1}. {item.name} - {price} {item.currency} - stock: {item.stock}")
        except ValueError:
            print(f"  {i+1}. {item.name} - не доступен - stock: {item.stock}")
    print()


def main():
    products = [
        Perfume("Tom Ford Lost Cherry", 28900, 3, 10, "Парфюмерия", "TF001", 50, "вишневый"),
        Perfume("Dior Sauvage", 12900, 12, 15, "Парфюмерия", "DIOR001", 100, "древесный"),
        Perfume("Chanel Coco", 18500, 0, 5, "Парфюмерия", "CH001", 75, "цветочный"),
        Skincare("La Roche-Posay", 2450, 25, 0, "Уход", "LRP001", "чувствительная", "церамиды"),
        Skincare("The Ordinary", 1890, 40, 0, "Уход", "TO001", "жирная", "ниацинамид"),
        Makeup("Dior Помада", 3850, 15, 5, "Макияж", "DIOR002", "999 красный", "матовая"),
        Makeup("Armani Тональный", 6890, 4, 0, "Макияж", "ARMANI002", "4.5 бежевый", "жидкий"),
    ]
    
    catalog = ProductCatalog()
    for p in products:
        catalog.add(p)

    print("1. НАЧАЛЬНЫЙ КАТАЛОГ")
    print_catalog(catalog)

    print("2. СОРТИРОВКА ПО ЦЕНЕ")
    sorted_catalog = ProductCatalog()
    for p in sorted(catalog.get_all(), key=by_price):
        sorted_catalog.add(p)
    print_catalog(sorted_catalog)

    print("3. СОРТИРОВКА ПО НАЗВАНИЮ")
    sorted_catalog = ProductCatalog()
    for p in sorted(catalog.get_all(), key=by_name):
        sorted_catalog.add(p)
    print_catalog(sorted_catalog)

    print("4. СОРТИРОВКА ПО КАТЕГОРИИ И ЦЕНЕ")
    sorted_catalog = ProductCatalog()
    for p in sorted(catalog.get_all(), key=by_category_then_price):
        sorted_catalog.add(p)
    print_catalog(sorted_catalog)

    print("5. ФИЛЬТР: ТОВАРЫ В НАЛИЧИИ")
    filtered = catalog.filter_by(is_available)
    print_catalog(filtered)

    print("6. ФИЛЬТР: ТОВАРЫ СО СКИДКОЙ")
    filtered = catalog.filter_by(has_discount)
    print_catalog(filtered)

    print("7. MAP: НАЗВАНИЯ ТОВАРОВ")
    names = list(map(lambda x: x.name, catalog.get_all()))
    for i, name in enumerate(names):
        print(f"  {i+1}. {name}")
    print()

    print("8. ФАБРИКА ФУНКЦИЙ: ФИЛЬТР ПО ЦЕНЕ <= 5000")
    price_filter = make_price_filter(5000)
    filtered = catalog.filter_by(price_filter)
    print_catalog(filtered)

    print("9. ЦЕПОЧКА ОПЕРАЦИЙ (filter -> sort -> map)")
    result = (catalog
              .filter_by(is_available)
              .sort_by(by_price)
              .map_to(lambda x: f"{x.name} - {x.calculate_price()} {x.currency}"))
    for i, item in enumerate(result):
        print(f"  {i+1}. {item}")
    print()

    print("10. CALLABLE-ОБЪЕКТ КАК СТРАТЕГИЯ")
    report = StatusReportStrategy()
    for item in catalog.get_all():
        print(f"  {report(item)}")
    print()

    print("11. CALLABLE-ОБЪЕКТ КАК СТРАТЕГИЯ (ПРИМЕНЕНИЕ СКИДКИ 20%)")
    discount = DiscountStrategy(20)
    test_catalog = ProductCatalog()
    for p in catalog.get_all():
        test_catalog.add(p)
    test_catalog.apply(discount)
    
    for item in test_catalog.get_all():
        try:
            print(f"  {item.name}: {item.calculate_price()} {item.currency} (скидка {item.discount}%)")
        except ValueError:
            print(f"  {item.name}: не доступен")
    print()

    print("12. МЕТОДЫ COLLECTION: filter_by по типу")
    perfumes = catalog.filter_by(is_perfume)
    print_catalog(perfumes)

    print("13. МЕТОД collection.sort_by (lambda)")
    catalog.sort_by(lambda x: x.stock, reverse=True)
    print_catalog(catalog)


if __name__ == "__main__":
    main()