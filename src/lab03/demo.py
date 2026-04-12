from lab03.base import Product
from lab03.models import Perfume, Skincare, Makeup
from lab03.collection import ProductCatalog


def main():    
    print("\n1. СОЗДАНИЕ ОБЪЕКТОВ")
    
    products = [
        Product("Пробник", 500, 20, 0, "Разное", "P001"),
        Perfume("Tom Ford Lost Cherry", 39900, 5, 0, "Парфюмерия", "TF001", 50, "вишневый"),
        Perfume("Dior Sauvage", 14800, 12, 10, "Парфюмерия", "DIOR001", 100, "древесный"),
        Skincare("La Roche-Posay Крем", 2450, 25, 0, "Уход", "LRP001", "чувствительная", "церамиды"),
        Skincare("The Ordinary Сыворотка", 1890, 40, 0, "Уход", "TO001", "жирная", "ниацинамид"),
        Makeup("Dior Помада", 3850, 15, 5, "Макияж", "DIOR002", "999 красный", "матовая"),
        Makeup("Armani Тональный", 6890, 4, 0, "Макияж", "ARMANI002", "4.5 бежевый", "жидкий"),
    ]
    
    catalog = ProductCatalog()
    for p in products:
        catalog.add(p)
        print(f"  - {p}")
    
    print("\n2. ПОЛИМОРФИЗМ - calculate_price()")
    
    for p in catalog:
        print(p.name, "-", p.calculate_price(), p.currency)
    
    print("\n3. НОВЫЕ МЕТОДЫ")
    
    for p in catalog:
        if isinstance(p, Perfume):
            print(f"   {p.name}: цена за мл = {p.get_price_per_ml()} {p.currency}")
        elif isinstance(p, Skincare):
            print(f"   {p.name}: {p.get_skin_compatibility()}")
        elif isinstance(p, Makeup):
            limited = "ЛИМИТИРОВАНА" if p.is_limited_edition() else "не лимитирована"
            print(f"   {p.name}: коллекция {limited}")
    
    print("\n4. ФИЛЬТРАЦИЯ ПО ТИПУ")
    
    perfumes = [p for p in catalog if isinstance(p, Perfume)]
    skincare = [p for p in catalog if isinstance(p, Skincare)]
    makeup = [p for p in catalog if isinstance(p, Makeup)]
    
    print(f"   Парфюм: {len(perfumes)} товаров")
    for p in perfumes:
        print(f" - {p.name} ({p.volume}мл, {p.fragrance_type})")
    
    print(f"\n   Уход за кожей: {len(skincare)} товаров")
    for p in skincare:
        print(f" - {p.name} (для {p.skin_type} кожи)")
    
    print(f"\n   Макияж: {len(makeup)} товаров")
    for p in makeup:
        print(f" - {p.name} (оттенок: {p.shade})")
    
    print("\n5. ИНТЕГРАЦИЯ С КОЛЛЕКЦИЕЙ")
    
    print("   Все товары дороже 5000 ₽:")
    expensive = catalog.get_expensive_products(5000)
    for p in expensive:
        print(f"  - {p.name}: {p.price} {p.currency}")
    
    print("\n6. Статистика каталога:")
    print(f"     Всего товаров: {len(catalog)}")
    print(f"     Активных товаров: {len(catalog.get_active_products())}")
    print(f"     Товаров в наличии: {len(catalog.get_available_products())}")
    print(f"     Товаров со скидкой: {len(catalog.get_products_with_discount())}")


if __name__ == "__main__":
    main()