from typing import List, Optional, Callable, Any
from lab03.base import Product


class ProductCatalog:
    
    def __init__(self):
        self._items: List[Product] = []
    
    def find_by_id(self, product_id: str) -> Optional[Product]:
        for item in self._items:
            if item.product_id == product_id:
                return item
        return None

    def add(self, item: Product) -> None:
        if not hasattr(item, 'calculate_price'):
            raise TypeError("Объект должен поддерживать интерфейс PriceCalculable")
        
        if self.find_by_id(item.product_id) is not None:
            raise ValueError(f"Товар с ID '{item.product_id}' уже существует в каталоге")
        
        self._items.append(item)
    
    def remove(self, item: Product) -> None:
        if item not in self._items:
            raise ValueError("Товар не найден в каталоге")
        self._items.remove(item)
    
    def remove_at(self, index: int) -> Product:
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        return self._items.pop(index)
    
    def get_all(self) -> List[Product]:
        return self._items.copy()
    
    def find_by_name(self, name: str) -> List[Product]:
        name_lower = name.lower()
        return [item for item in self._items if name_lower in item.name.lower()]
    
    def find_by_category(self, category: str) -> List[Product]:
        category_lower = category.lower()
        return [item for item in self._items if item.category.lower() == category_lower]
    
    def __len__(self) -> int:
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
    
    def sort_by(self, key_func: Callable[[Product], Any], reverse: bool = False) -> 'ProductCatalog':
        self._items.sort(key=key_func, reverse=reverse)
        return self
    
    def filter_by(self, predicate: Callable[[Product], bool]) -> 'ProductCatalog':
        new_catalog = ProductCatalog()
        for item in self._items:
            if predicate(item):
                new_catalog.add(item)
        return new_catalog
    
    def apply(self, func: Callable[[Product], Any]) -> 'ProductCatalog':
        for item in self._items:
            func(item)
        return self
    
    def map_to(self, func: Callable[[Product], Any]) -> list:
        return list(map(func, self._items))
    
    def get_available_products(self) -> 'ProductCatalog':
        new_catalog = ProductCatalog()
        for item in self._items:
            if item.stock > 0:
                new_catalog.add(item)
        return new_catalog
    
    def get_expensive_products(self, threshold: float = 5000) -> 'ProductCatalog':
        new_catalog = ProductCatalog()
        for item in self._items:
            if item.price > threshold:
                new_catalog.add(item)
        return new_catalog