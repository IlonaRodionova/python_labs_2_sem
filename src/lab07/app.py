"""
Бизнес-логика приложения. Управление коллекцией товаров.
"""

from typing import List, Callable, Any
from lab03.base import Product
from lab03.models import Perfume, Skincare, Makeup
from lab05.strategies import (
    is_available, has_discount, is_perfume, is_skincare, is_makeup
)
from lab07.collection import ProductCatalog
from lab07.exceptions import DuplicateItemError, ItemNotFoundError, InvalidDataError
from lab07.storage import save, load


DATA_FILE = "products.json"


class ProductApp:
    """
    Основной класс приложения. Управляет коллекцией и бизнес-логикой.
    """
    
    def __init__(self):
        """Инициализирует приложение: загружает данные из файла."""
        self._catalog = ProductCatalog()
        self._load_data()
    
    def _load_data(self) -> None:
        """Загружает данные из файла при запуске."""
        products = load(DATA_FILE)
        for product in products:
            try:
                self._catalog.add(product)
            except ValueError:
                pass
    
    def _save_data(self) -> None:
        """Сохраняет данные в файл."""
        save(self._catalog.get_all(), DATA_FILE)
    
    def get_all_products(self) -> List[Product]:
        """Возвращает все товары из каталога."""
        return self._catalog.get_all()
    
    def add_product(
        self,
        product_type: str,
        name: str,
        price: float,
        stock: int,
        discount: int,
        category: str,
        product_id: str,
        **kwargs
    ) -> Product:
        """
        Добавляет новый товар в каталог.
        """
        try:
            if product_type == "Perfume":
                product = Perfume(
                    name=name,
                    price=price,
                    stock=stock,
                    discount=discount,
                    category=category,
                    product_id=product_id,
                    volume=kwargs.get("volume", 0),
                    fragrance_type=kwargs.get("fragrance_type", "")
                )
            elif product_type == "Skincare":
                product = Skincare(
                    name=name,
                    price=price,
                    stock=stock,
                    discount=discount,
                    category=category,
                    product_id=product_id,
                    skin_type=kwargs.get("skin_type", ""),
                    active_ingredient=kwargs.get("active_ingredient", "")
                )
            elif product_type == "Makeup":
                product = Makeup(
                    name=name,
                    price=price,
                    stock=stock,
                    discount=discount,
                    category=category,
                    product_id=product_id,
                    shade=kwargs.get("shade", ""),
                    texture=kwargs.get("texture", "")
                )
            else:
                product = Product(
                    name=name,
                    price=price,
                    stock=stock,
                    discount=discount,
                    category=category,
                    product_id=product_id
                )
            
            self._catalog.add(product)
            self._save_data()
            return product
        
        except ValueError as e:
            raise InvalidDataError(str(e))
    
    def remove_product(self, product_id: str) -> Product:
        """
        Удаляет товар из каталога.
        """
        product = self._catalog.find_by_id(product_id)
        if product is None:
            raise ItemNotFoundError(f"Товар с ID '{product_id}' не найден")
        
        self._catalog.remove(product)
        self._save_data()
        return product
    
    def find_by_id(self, product_id: str) -> Product:
        """Находит товар по ID."""
        product = self._catalog.find_by_id(product_id)
        if product is None:
            raise ItemNotFoundError(f"Товар с ID '{product_id}' не найден")
        return product
    
    def find_by_name(self, name: str) -> List[Product]:
        """Находит товары по названию (частичное совпадение)."""
        return self._catalog.find_by_name(name)
    
    def filter_by(self, predicate: Callable[[Product], bool]) -> List[Product]:
        """Фильтрует товары по предикату."""
        filtered = self._catalog.filter_by(predicate)
        return filtered.get_all()
    
    def sort_by(self, key_func: Callable[[Product], Any], reverse: bool = False) -> List[Product]:
        """Сортирует товары по ключевой функции."""
        products = self._catalog.get_all()
        return sorted(products, key=key_func, reverse=reverse)
    
    def get_available_products(self) -> List[Product]:
        """Возвращает товары в наличии."""
        return self.filter_by(is_available)
    
    def get_products_with_discount(self) -> List[Product]:
        """Возвращает товары со скидкой."""
        return self.filter_by(has_discount)
    
    def get_perfumes(self) -> List[Product]:
        """Возвращает только парфюм."""
        return self.filter_by(is_perfume)
    
    def get_skincare(self) -> List[Product]:
        """Возвращает только уход за кожей."""
        return self.filter_by(is_skincare)
    
    def get_makeup(self) -> List[Product]:
        """Возвращает только макияж."""
        return self.filter_by(is_makeup)
    
    def apply_discount_to_all(self, percent: int) -> None:
        """Применяет скидку ко всем товарам."""
        for product in self._catalog.get_all():
            if product.discount < percent:
                product.discount = percent
        self._save_data()
    
    def close(self) -> None:
        """Сохраняет данные перед выходом."""
        self._save_data()