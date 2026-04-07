from lab02.model import Product
from lab02.collection import ProductCatalog


def print_catalog(catalog: ProductCatalog, name: str = "Каталог"):
    print(f"\n{name} (всего товаров: {len(catalog)}):")
    if len(catalog) == 0:
        print("  (пусто)")
    else:
        for i, product in enumerate(catalog):
            stock_str = f" [{product.stock} шт.]" if product.stock > 0 else " [нет в наличии]"
            discount_str = f" (скидка {product.discount}%)" if product.discount > 0 else ""
            
            if product.stock > 0:
                final_price = product.get_final_price()
                print(f"  {i}. {product.name} - {final_price} {product.currency}{discount_str}{stock_str}")
            else:
                print(f"  {i}. {product.name} - НЕ ДОСТУПЕН {stock_str}")
    print()


def main():
    print("Контейнерный класс ProductCatalog")
    print("Предметная область: Товары (Парфюмерия и косметика)")
    print("Магазин: Золотое Яблоко")
    
    print("\nСоздание товаров:")    
    products = [
        Product("Tom Ford Lost Cherry EDP", 28900, 5, 0, "Парфюмерия", "TF001"),
        Product("Dior Sauvage EDP", 12900, 12, 10, "Парфюмерия", "DIOR001"),
        Product("Chanel Coco Mademoiselle", 18500, 8, 5, "Парфюмерия", "CHANEL001"),
        Product("Lancome La Vie Est Belle", 11200, 0, 15, "Парфюмерия", "LAN001"),
        Product("YSL Libre EDP", 13900, 7, 0, "Парфюмерия", "YSL001"),
        Product("Armani Acqua di Gio", 11900, 3, 20, "Парфюмерия", "ARMANI001"),
        Product("Крем для лица La Roche-Posay", 2450, 25, 0, "Уход за лицом", "LRP001"),
        Product("Сыворотка The Ordinary", 1890, 40, 0, "Уход за лицом", "TO001"),
        Product("Шампунь Kerastase", 4250, 10, 10, "Уход за волосами", "KER001"),
        Product("Маска для волос Moroccanoil", 3890, 6, 5, "Уход за волосами", "MOR001"),
        Product("Помада Dior Rouge", 3850, 15, 0, "Макияж", "DIOR002"),
        Product("Тональный крем Armani", 6890, 4, 0, "Макияж", "ARMANI002"),
    ]
    
    catalog = ProductCatalog()
    for product in products:
        catalog.add(product)
        status = "(в наличии)" if product.stock > 0 else "(нет в наличии, деактивирован)"
        print(f"  {status} {product.name} - {product.price} {product.currency}")
    
    print_catalog(catalog, "Каталог ЗЯ")
    
    print("1. Базовые операции")
    
    print("Проверка ограничения на дубликаты:")
    try:
        duplicate = Product("Tom Ford Lost Cherry EDP", 28900, 5, 0, "Парфюмерия", "TF001")
        catalog.add(duplicate)
        print("ОШИБКА: Дубликат был добавлен!")
    except ValueError as e:
        print(f"Ограничение сработало: {e}")
    
    print("Проверка типа добавляемого объекта:")
    try:
        catalog.add("Это строка, а не товар")
        print("ОШИБКА: Строка была добавлена!")
    except TypeError as e:
        print(f"Проверка типа сработала: {e}")
    
    print("Удаление товара:")
    to_remove = products[7]
    print(f"Удаляем: {to_remove.name}")
    catalog.remove(to_remove)
    print_catalog(catalog, "Каталог после удаления")
    
    print("2. Поиск и итерация")
    
    print("Поиск по ID 'DIOR001':")
    found = catalog.find_by_id("DIOR001")
    if found:
        print(f"Найден: {found.name} - {found.price} {found.currency}")
    
    print("Поиск по названию (частичное совпадение 'Dior'):")
    found_products = catalog.find_by_name("Dior")
    for p in found_products:
        print(f"  • {p.name} - {p.price} {p.currency}")
    
    print("Поиск по категории 'Уход за волосами':")
    hair_products = catalog.find_by_category("Уход за волосами")
    for p in hair_products:
        print(f"  • {p.name} - {p.price} {p.currency}")
    
    print("Поиск товаров от 3000 до 7000 ₽:")
    mid_price = catalog.find_by_price_range(3000, 7000)
    for p in mid_price:
        print(f"  • {p.name} - {p.price} {p.currency}")
    
    print(f"Количество товаров в каталоге: {len(catalog)}")
    
    print("Итерация по каталогу (for item in catalog):")
    for i, product in enumerate(catalog):
        if i < 5:
            if product.stock > 0:
                final_price = product.get_final_price()
                print(f"  {i+1}. {product.name}: {final_price} {product.currency}")
            else:
                print(f"  {i+1}. {product.name}: НЕТ В НАЛИЧИИ")
    if len(catalog) > 5:
        print(f"  ... и еще {len(catalog) - 5} товаров")
    
    print("\n3. Индексация, сортировка и фильтрация")
    
    print("Доступ по индексу (__getitem__):")
    print(f"  catalog[0] = {catalog[0].name}")
    print(f"  catalog[2] = {catalog[2].name}")
    print(f"  catalog[-1] = {catalog[-1].name}")
    
    print("\nСрезы коллекции:")
    slice_result = catalog[1:4]
    print(f"  catalog[1:4]: {[p.name for p in slice_result]}")
    
    print("\nУдаление по индексу (remove_at):")
    removed = catalog.remove_at(2)
    print(f"  Удален товар по индексу 2: {removed.name}")
    print_catalog(catalog, "Каталог после удаления по индексу")
    
    print("\nСортировка по цене (от дешевых к дорогим):")
    catalog.sort_by_price()
    for p in catalog[:5]:
        if p.stock > 0:
            print(f"  {p.name}: {p.price} {p.currency}")
        else:
            print(f"  {p.name}: {p.price} {p.currency} (нет в наличии)")
    print("  ...")
    
    print("\nСортировка по названию (A-Z):")
    catalog.sort_by_name()
    for p in catalog[:5]:
        print(f"  {p.name}")
    print("  ...")
    
    print("\nСортировка по размеру скидки (максимальная первая):")
    catalog.sort_by_discount(reverse=True)
    for p in catalog:
        if p.discount > 0 and p.stock > 0:
            print(f"  {p.name}: скидка {p.discount}% -> {p.get_final_price()} {p.currency}")
        elif p.discount > 0:
            print(f"  {p.name}: скидка {p.discount}% (нет в наличии)")
    
    print("\nФильтрация: активные товары:")
    active = catalog.get_active_products()
    print_catalog(active, "Активные товары")
    
    print("\nФильтрация: товары в наличии (stock > 0):")
    available = catalog.get_available_products()
    print_catalog(available, "Товары в наличии")
    
    print("\nФильтрация: товары со скидкой:")
    discounted = catalog.get_products_with_discount()
    print_catalog(discounted, "Товары со скидкой")
    
    print("\nФильтрация: дорогие товары (цена > 10000 ₽):")
    expensive = catalog.get_expensive_products(10000)
    print_catalog(expensive, "Премиум товары")
    
    print("\n4. Сложные запросы")
    
    print("\nАктивные парфюмерные товары со скидкой:")
    parfume_with_discount = (catalog
                             .get_by_category("Парфюмерия")
                             .get_products_with_discount()
                             .get_active_products())
    
    for p in parfume_with_discount:
        if p.stock > 0:
            print(f"  • {p.name}: {p.price} {p.currency} -> {p.get_final_price()} {p.currency} (скидка {p.discount}%)")
        else:
            print(f"  • {p.name}: {p.price} {p.currency} (скидка {p.discount}%, нет в наличии)")
    
    print("\nТовары для лица в наличии:")
    face_available = catalog.get_by_category("Уход за лицом").get_available_products()
    for p in face_available:
        print(f"  • {p.name} - {p.price} {p.currency} (в наличии: {p.stock} шт.)")
    
    print("\n5. Симуляция покупки")
    print("Клиент хочет купить: Dior Sauvage EDP")
    dior = catalog.find_by_id("DIOR001")
    if dior and dior.stock > 0:
        print(f"  Товар найден: {dior.name}")
        print(f"  Цена: {dior.price} {dior.currency}")
        print(f"  Скидка: {dior.discount}%")
        print(f"  Итоговая цена: {dior.get_final_price()} {dior.currency}")
        dior.reduce_stock(1)
        print(f"  Покупка совершена! Остаток на складе: {dior.stock} шт.")
    
    print("\nПроверка автоматической деактивации при отсутствии товара:")
    lancome = catalog.find_by_id("LAN001")
    if lancome:
        print(f"Товар: {lancome.name}")
        print(f"Наличие: {lancome.stock} шт.")
        print(f"Активен: {lancome._active}")
        print(f"При попытке получить цену: ")
        try:
            lancome.get_final_price()
        except ValueError as e:
            print(f"Ошибка: {e}")
    
    print("\nСтатистика каталога:")
    print(f"  • Всего товаров: {len(catalog)}")
    print(f"  • В наличии: {len(catalog.get_available_products())}")
    print(f"  • Со скидкой: {len(catalog.get_products_with_discount())}")
    print(f"  • Премиум (>10000₽): {len(catalog.get_expensive_products(10000))}")


if __name__ == "__main__":
    main()