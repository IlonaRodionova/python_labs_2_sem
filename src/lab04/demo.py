from lab04.models import Perfume, Skincare, Makeup
from lab04.collection import ProductCatalog
from lab04.interfaces import PriceCalculable, Displayable, Discountable


def print_interface_info(items, interface_name):
    """Универсальная функция, работающая через интерфейс Displayable"""
    print(f"\n {interface_name}")
    for item in items:
        if isinstance(item, Displayable):
            print(f"  {item.get_display_info()}")


def calculate_all_prices(items):
    """Универсальная функция, работающая через интерфейс PriceCalculable"""
    total = 0
    for item in items:
        if isinstance(item, PriceCalculable):
            total += item.calculate_price()
    return total


def main():

    print("1.СОЗДАНИЕ ОБЪЕКТОВ")
    
    products = [
        Perfume("Tom Ford Lost Cherry", 28900, 5, 0, "Парфюмерия", "TF001", 50, "вишневый"),
        Perfume("Dior Sauvage", 12900, 12, 10, "Парфюмерия", "DIOR001", 100, "древесный"),
        Skincare("La Roche-Posay Крем", 2450, 25, 0, "Уход", "LRP001", "чувствительная", "церамиды"),
        Skincare("The Ordinary Сыворотка", 1890, 40, 0, "Уход", "TO001", "жирная", "ниацинамид"),
        Makeup("Dior Помада", 3850, 15, 5, "Макияж", "DIOR002", "999 красный", "матовая"),
        Makeup("Armani Тональный", 6890, 4, 0, "Макияж", "ARMANI002", "4.5 бежевый", "жидкий"),
    ]
    
    catalog = ProductCatalog()
    for p in products:
        catalog.add(p)
        print(f" {p}")

    print("\n2.ПРОВЕРКА РЕАЛИЗАЦИИ ИНТЕРФЕЙСОВ (isinstance)")
    
    for p in catalog:
        interfaces = []
        if isinstance(p, PriceCalculable):
            interfaces.append("PriceCalculable")
        if isinstance(p, Displayable):
            interfaces.append("Displayable")
        if isinstance(p, Discountable):
            interfaces.append("Discountable")
        print(f"  {p.name}: реализует {', '.join(interfaces)}")
    

    print("\n3.ВЫВОД ЧЕРЕЗ ИНТЕРФЕЙС Displayable")
    print_interface_info(catalog, "Информация о товарах")
    

    print("\n4.ПОДСЧЕТ СТОИМОСТИ ЧЕРЕЗ ИНТЕРФЕЙС PriceCalculable")
    total = calculate_all_prices(catalog)
    print(f"  Общая стоимость всех товаров: {total} ₽")
    

    print("\n5.ФИЛЬТРАЦИЯ КОЛЛЕКЦИИ ПО ИНТЕРФЕЙСУ")
    
    discountable = catalog.get_discountable()
    print(f"  Товары со скидкой (Discountable): {len(discountable)}")
    for p in discountable:
        print(f"    - {p.name}: скидка {p.get_discount_percent()}%")
    

    print("\n6.ПОЛИМОРФИЗМ ЧЕРЕЗ ИНТЕРФЕЙС")
    print("  Вызов calculate_price() у разных объектов (без проверки типов):")
    
    for p in catalog:
        if isinstance(p, PriceCalculable):
            print(f"    {p.name}: {p.calculate_price()} ₽")
    


if __name__ == "__main__":
    main()