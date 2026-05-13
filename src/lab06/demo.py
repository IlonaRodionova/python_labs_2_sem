from lab03.base import Product
from lab03.models import Perfume, Skincare, Makeup
from lab06.container import TypedCollection, Displayable, Scorable


def main():    
    print("\n1. ОБЫЧНАЯ GENERIC КОЛЛЕКЦИЯ")
    products = [
        Perfume("Tom Ford Lost Cherry", 28900, 3, 10, "Парфюмерия", "TF001", 50, "вишневый"),
        Perfume("Dior Sauvage", 12900, 12, 15, "Парфюмерия", "DIOR001", 100, "древесный"),
        Skincare("La Roche-Posay", 2450, 25, 0, "Уход", "LRP001", "чувствительная", "церамиды"),
        Makeup("Dior Помада", 3850, 15, 5, "Макияж", "DIOR002", "999 красный", "матовая"),
    ]
    
    collection = TypedCollection[Product]()
    for p in products:
        collection.add(p)
        print(f"добавлен: {p.name}")
    
    print(f"\n  Всего элементов: {len(collection)}")
    print("Содержимое коллекции:")
    for i, item in enumerate(collection.get_all()):
        print(f"    {i+1}. {item.name}")
    

    print("\n2. МЕТОДЫ FIND, FILTER, MAP")
    
    print("\n  find(): поиск товара с ценой > 10000")
    expensive = collection.find(lambda x: x.price > 10000)
    if expensive:
        print(f"    Найден: {expensive.name} - {expensive.price} ₽")
    
    print("\n  find(): поиск товара с ценой > 100000 (не найден)")
    not_found = collection.find(lambda x: x.price > 100000)
    print(f"    Результат: {not_found}")
    
    print("\n  filter(): товары со скидкой")
    discounted = collection.filter(lambda x: x.discount > 0)
    for item in discounted:
        print(f"    {item.name} - скидка {item.discount}%")
    
    print("\n  map(): извлечение названий товаров")
    names = collection.map(lambda x: x.name)
    for i, name in enumerate(names):
        print(f"    {i+1}. {name}")
    
    print("\n  map(): извлечение цен (тип результата float)")
    prices = collection.map(lambda x: x.price)
    for i, price in enumerate(prices):
        print(f"    {names[i]}: {price} ₽")
    

    print("\n3. PROTOCOL И STRUCTURAL TYPING")
    print("\n  Сценарий 1: TypedCollection с ограничением Displayable")
    
    displayable_collection = TypedCollection[Displayable]()
    
    displayable_collection.add(products[0])  # Perfume
    displayable_collection.add(products[2])  # Skincare
    displayable_collection.add(products[3])  # Makeup
    
    print("  Вызов метода display() для каждого объекта:")
    for item in displayable_collection.get_all():
        print(f"    {item.display()}")
    
    print("\n  Сценарий 2: TypedCollection с ограничением Scorable")
    
    scorable_collection = TypedCollection[Scorable]()
    
    scorable_collection.add(products[0])  # Perfume
    scorable_collection.add(products[1])  # Perfume
    scorable_collection.add(products[2])  # Skincare
    
    print("  Вызов метода score() для каждого объекта:")
    for item in scorable_collection.get_all():
        print(f"    {item.name}: {item.score()} ₽")
    
    print("\n  Сценарий 3: сортировка через map и filter с типизацией")
    
    print("  Товары дороже 5000:")
    expensive_items = collection.filter(lambda x: x.price > 5000)
    for item in expensive_items:
        print(f"    {item.name} - {item.price} ₽")
    
    print("\n  Имена и цены:")
    result = collection.map(lambda x: f"{x.name}: {x.price} ₽")
    for r in result:
        print(f"    {r}")

if __name__ == "__main__":
    main()