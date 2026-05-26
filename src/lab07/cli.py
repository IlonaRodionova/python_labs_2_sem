"""
Консольный интерфейс пользователя. Отвечает за ввод/вывод и меню.
"""

from typing import List
from lab03.base import Product
from lab03.models import Perfume, Skincare, Makeup
from lab05.strategies import by_name, by_price, by_stock, by_discount
from lab07.app import ProductApp
from lab07.exceptions import DuplicateItemError, ItemNotFoundError, InvalidDataError


def print_product(product: Product, index: int = None) -> None:
    """
    Выводит информацию о товаре.
    
    Args:
        product: объект товара
        index: порядковый номер (опционально)
    """
    prefix = f"{index}. " if index is not None else ""
    try:
        price = product.calculate_price()
        status = "доступен" if product.stock > 0 else "НЕТ В НАЛИЧИИ"
        print(f"{prefix}{product.name} | {price} {product.currency} | {status} | stock: {product.stock}")
    except ValueError:
        print(f"{prefix}{product.name} | НЕ ДОСТУПЕН | stock: {product.stock}")


def print_products(products: List[Product], title: str) -> None:
    """
    Выводит список товаров с заголовком.
    
    Args:
        products: список товаров
        title: заголовок
    """
    print(f"\n{title}")
    print("-" * 50)
    if not products:
        print("  (пусто)")
    else:
        for i, product in enumerate(products, 1):
            print_product(product, i)
    print()


def get_yes_no(prompt: str) -> bool:
    """
    Запрашивает подтверждение да/нет.
    
    Args:
        prompt: текст запроса
    
    Returns:
        True если пользователь ввёл y, False иначе
    """
    answer = input(f"{prompt} (да/нет): ").lower()
    return answer == 'да'


def get_int_input(prompt: str, default: int = None) -> int:
    """
    Запрашивает целое число с обработкой ошибок.
    
    Args:
        prompt: текст запроса
        default: значение по умолчанию (если ввод пустой)
    
    Returns:
        введённое целое число
    """
    while True:
        try:
            value = input(prompt)
            if value == "" and default is not None:
                return default
            return int(value)
        except ValueError:
            print("Ошибка: введите целое число")


def get_float_input(prompt: str, default: float = None) -> float:
    """
    Запрашивает вещественное число с обработкой ошибок.
    
    Args:
        prompt: текст запроса
        default: значение по умолчанию (если ввод пустой)
    
    Returns:
        введённое вещественное число
    """
    while True:
        try:
            value = input(prompt)
            if value == "" and default is not None:
                return default
            return float(value)
        except ValueError:
            print("Ошибка: введите число")


def add_product_interactive(app: ProductApp) -> None:
    """
    Интерактивное добавление товара.
    
    Args:
        app: экземпляр приложения
    """
    print("\n--- ДОБАВЛЕНИЕ ТОВАРА ---")
    
    print("Типы товаров:")
    print("  1. Обычный товар")
    print("  2. Парфюм (Perfume)")
    print("  3. Уход за кожей (Skincare)")
    print("  4. Макияж (Makeup)")
    
    type_choice = get_int_input("Выберите тип (1-4): ")
    
    name = input("Название: ").strip()
    if not name:
        print("Ошибка: название не может быть пустым")
        return
    
    price = get_float_input("Цена: ")
    if price <= 0:
        print("Ошибка: цена должна быть положительной")
        return
    
    stock = get_int_input("Количество на складе: ")
    discount = get_int_input("Скидка (%): ", default=0)
    category = input("Категория: ").strip()
    product_id = input("ID товара: ").strip()
    
    if not product_id:
        print("Ошибка: ID не может быть пустым")
        return
    
    try:
        if type_choice == 2:
            volume = get_int_input("Объём (мл): ")
            fragrance_type = input("Тип аромата: ").strip()
            product = app.add_product(
                "Perfume", name, price, stock, discount, category, product_id,
                volume=volume, fragrance_type=fragrance_type
            )
        elif type_choice == 3:
            skin_type = input("Тип кожи: ").strip()
            active_ingredient = input("Активный компонент: ").strip()
            product = app.add_product(
                "Skincare", name, price, stock, discount, category, product_id,
                skin_type=skin_type, active_ingredient=active_ingredient
            )
        elif type_choice == 4:
            shade = input("Оттенок: ").strip()
            texture = input("Текстура: ").strip()
            product = app.add_product(
                "Makeup", name, price, stock, discount, category, product_id,
                shade=shade, texture=texture
            )
        else:
            product = app.add_product(
                "Product", name, price, stock, discount, category, product_id
            )
        
        print(f"\nТовар успешно добавлен:")
        print_product(product)
    
    except DuplicateItemError as e:
        print(f"\nОшибка: {e}")
    except InvalidDataError as e:
        print(f"\nОшибка в данных: {e}")


def remove_product_interactive(app: ProductApp) -> None:
    """
    Интерактивное удаление товара.
    
    Args:
        app: экземпляр приложения
    """
    print("\n--- УДАЛЕНИЕ ТОВАРА ---")
    product_id = input("Введите ID товара для удаления: ").strip()
    
    if not product_id:
        print("Ошибка: ID не может быть пустым")
        return
    
    try:
        product = app.find_by_id(product_id)
        print("\nНайден товар:")
        print_product(product)
        
        if get_yes_no(f"\nУдалить '{product.name}'?"):
            app.remove_product(product_id)
            print("Товар удалён")
        else:
            print("Удаление отменено")
    
    except ItemNotFoundError as e:
        print(f"\nОшибка: {e}")


def search_product_interactive(app: ProductApp) -> None:
    """
    Интерактивный поиск товара.
    
    Args:
        app: экземпляр приложения
    """
    print("\n--- ПОИСК ТОВАРА ---")
    print("1. По ID")
    print("2. По названию")
    
    choice = get_int_input("Выберите способ (1-2): ")
    
    if choice == 1:
        product_id = input("Введите ID: ").strip()
        try:
            product = app.find_by_id(product_id)
            print("\nРезультат:")
            print_product(product)
        except ItemNotFoundError as e:
            print(f"\nОшибка: {e}")
    
    elif choice == 2:
        name = input("Введите название (или часть): ").strip()
        products = app.find_by_name(name)
        print_products(products, f"Результаты поиска по '{name}':")
    
    else:
        print("Неверный выбор")


def filter_products_interactive(app: ProductApp) -> None:
    """
    Интерактивная фильтрация товаров.
    
    Args:
        app: экземпляр приложения
    """
    print("\n--- ФИЛЬТРАЦИЯ ТОВАРОВ ---")
    print("1. Только в наличии")
    print("2. Только со скидкой")
    print("3. Только парфюм")
    print("4. Только уход за кожей")
    print("5. Только макияж")
    
    choice = get_int_input("Выберите фильтр (1-5): ")
    
    if choice == 1:
        products = app.get_available_products()
        print_products(products, "ТОВАРЫ В НАЛИЧИИ:")
    elif choice == 2:
        products = app.get_products_with_discount()
        print_products(products, "ТОВАРЫ СО СКИДКОЙ:")
    elif choice == 3:
        products = app.get_perfumes()
        print_products(products, "ПАРФЮМ:")
    elif choice == 4:
        products = app.get_skincare()
        print_products(products, "УХОД ЗА КОЖЕЙ:")
    elif choice == 5:
        products = app.get_makeup()
        print_products(products, "МАКИЯЖ:")
    else:
        print("Неверный выбор")


def sort_products_interactive(app: ProductApp) -> None:
    """
    Интерактивная сортировка товаров.
    
    Args:
        app: экземпляр приложения
    """
    print("\n--- СОРТИРОВКА ТОВАРОВ ---")
    print("1. По названию")
    print("2. По цене (от дешёвых к дорогим)")
    print("3. По цене (от дорогих к дешёвым)")
    print("4. По количеству на складе")
    print("5. По скидке")
    
    choice = get_int_input("Выберите стратегию (1-5): ")
    
    if choice == 1:
        products = app.sort_by(by_name)
        print_products(products, "СОРТИРОВКА ПО НАЗВАНИЮ:")
    elif choice == 2:
        products = app.sort_by(by_price)
        print_products(products, "СОРТИРОВКА ПО ЦЕНЕ (от дешёвых к дорогим):")
    elif choice == 3:
        products = app.sort_by(by_price, reverse=True)
        print_products(products, "СОРТИРОВКА ПО ЦЕНЕ (от дорогих к дешёвым):")
    elif choice == 4:
        products = app.sort_by(by_stock, reverse=True)
        print_products(products, "СОРТИРОВКА ПО КОЛИЧЕСТВУ (по убыванию):")
    elif choice == 5:
        products = app.sort_by(by_discount, reverse=True)
        print_products(products, "СОРТИРОВКА ПО СКИДКЕ (по убыванию):")
    else:
        print("Неверный выбор")


def apply_discount_interactive(app: ProductApp) -> None:
    """
    Интерактивное применение скидки ко всем товарам.
    
    Args:
        app: экземпляр приложения
    """
    print("\n--- ПРИМЕНЕНИЕ СКИДКИ ---")
    percent = get_int_input("Введите процент скидки (0-100): ")
    
    if percent < 0 or percent > 100:
        print("Ошибка: процент должен быть от 0 до 100")
        return
    
    if get_yes_no(f"Применить скидку {percent}% ко всем товарам?"):
        app.apply_discount_to_all(percent)
        print(f"Скидка {percent}% применена ко всем товарам")
    else:
        print("Операция отменена")


def show_all_products(app: ProductApp) -> None:
    """
    Показывает все товары.
    
    Args:
        app: экземпляр приложения
    """
    products = app.get_all_products()
    print_products(products, "ВСЕ ТОВАРЫ:")


def main() -> None:
    """
    Главная функция приложения. Запускает цикл меню.
    """
    app = ProductApp()
    
    print("\n" + "=" * 60)
    print("ДОБРО ПОЖАЛОВАТЬ В КАТАЛОГ ТОВАРОВ")
    print("Интернет-магазин 'Золотое Яблоко'")
    print("=" * 60)
    
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Показать все товары")
        print("2. Добавить товар")
        print("3. Удалить товар")
        print("4. Найти товар")
        print("5. Фильтровать товары")
        print("6. Сортировать товары")
        print("7. Применить скидку ко всем")
        print("0. Выход")
        
        try:
            choice = int(input("\nВыберите пункт: "))
        except ValueError:
            print("Ошибка: введите число от 0 до 7")
            continue
        
        if choice == 1:
            show_all_products(app)
        elif choice == 2:
            add_product_interactive(app)
        elif choice == 3:
            remove_product_interactive(app)
        elif choice == 4:
            search_product_interactive(app)
        elif choice == 5:
            filter_products_interactive(app)
        elif choice == 6:
            sort_products_interactive(app)
        elif choice == 7:
            apply_discount_interactive(app)
        elif choice == 0:
            if get_yes_no("Сохранить изменения и выйти?"):
                app.close()
                print("Данные сохранены. До свидания!")
            else:
                print("Выход без сохранения. До свидания!")
            break
        else:
            print("Неверный пункт меню. Введите число от 0 до 7")


if __name__ == "__main__":
    main()