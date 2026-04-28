from lab04.interfaces import PriceCalculable, Displayable, Discountable
from lab04.models import Perfume, Skincare, Makeup


class ProductCatalog:
    
    def __init__(self):
        self._items = []
    
    def find_by_id(self, product_id):
        for item in self._items:
            if item.product_id == product_id:
                return item
        return None

    def add(self, item):
        if not hasattr(item, 'calculate_price'):
            raise TypeError(f"Объект должен поддерживать интерфейс PriceCalculable")
        
        if self.find_by_id(item.product_id) is not None:
            raise ValueError(f"Товар с ID '{item.product_id}' уже существует в каталоге")
        
        self._items.append(item)
    
    def remove(self, item):
        if item not in self._items:
            raise ValueError("Товар не найден в каталоге")
        self._items.remove(item)
    
    def remove_at(self, index):
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        return self._items.pop(index)
    
    def get_all(self):
        return self._items.copy()
    
    def find_by_name(self, name):
        name_lower = name.lower()
        return [item for item in self._items if name_lower in item.name.lower()]
    
    def find_by_category(self, category):
        category_lower = category.lower()
        return [item for item in self._items if item.category.lower() == category_lower]
    
    def find_by_price_range(self, min_price, max_price):
        return [item for item in self._items if min_price <= item.price <= max_price]
    
    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            new_catalog = ProductCatalog()
            for item in self._items[index]:
                new_catalog.add(item)
            return new_catalog
        
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        
        if index < 0:
            index = len(self._items) + index
        
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        
        return self._items[index]
    
    def __contains__(self, item):
        return item in self._items
    
    def __str__(self):
        if not self._items:
            return "ProductCatalog (пусто)"
        return f"ProductCatalog ({len(self._items)} товаров)"
    
    def sort(self, key=None, reverse=False):
        if key is None:
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)
    
    def sort_by_name(self, reverse=False):
        self._items.sort(key=lambda p: p.name.lower(), reverse=reverse)
    
    def sort_by_price(self, reverse=False):
        self._items.sort(key=lambda p: p.price, reverse=reverse)
    
    def sort_by_stock(self, reverse=False):
        self._items.sort(key=lambda p: p.stock, reverse=reverse)
    
    def sort_by_discount(self, reverse=False):
        self._items.sort(key=lambda p: p.discount, reverse=reverse)
    
    def get_active_products(self):
        new_catalog = ProductCatalog()
        for item in self._items:
            if item._active:
                new_catalog.add(item)
        return new_catalog
    
    def get_available_products(self):
        new_catalog = ProductCatalog()
        for item in self._items:
            if item.stock > 0:
                new_catalog.add(item)
        return new_catalog
    
    def get_products_with_discount(self):
        new_catalog = ProductCatalog()
        for item in self._items:
            if item.discount > 0:
                new_catalog.add(item)
        return new_catalog
    
    def get_expensive_products(self, threshold=5000):
        new_catalog = ProductCatalog()
        for item in self._items:
            if item.price > threshold:
                new_catalog.add(item)
        return new_catalog
    
    def get_by_category(self, category):
        new_catalog = ProductCatalog()
        for item in self._items:
            if item.category.lower() == category.lower():
                new_catalog.add(item)
        return new_catalog
    
    # НОВЫЕ МЕТОДЫ ДЛЯ ЛР-4: фильтрация по интерфейсам
    def get_price_calculable(self):
        """Возвращает новую коллекцию объектов, реализующих PriceCalculable"""
        new_catalog = ProductCatalog()
        for item in self._items:
            if isinstance(item, PriceCalculable):
                new_catalog.add(item)
        return new_catalog
    
    def get_displayable(self):
        """Возвращает новую коллекцию объектов, реализующих Displayable"""
        new_catalog = ProductCatalog()
        for item in self._items:
            if isinstance(item, Displayable):
                new_catalog.add(item)
        return new_catalog
    
    def get_discountable(self):
        """Возвращает новую коллекцию объектов, реализующих Discountable"""
        new_catalog = ProductCatalog()
        for item in self._items:
            if isinstance(item, Discountable):
                new_catalog.add(item)
        return new_catalog