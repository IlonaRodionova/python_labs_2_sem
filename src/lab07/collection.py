"""
Коллекция для лабораторной работы №7.
Использует Product из lab03.base.
"""

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
        if not isinstance(item, Product):
            raise TypeError(f"Можно добавлять только объекты Product, получен {type(item).__name__}")
        
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
    
    def __contains__(self, item: Product) -> bool:
        return item in self._items
    
    def filter_by(self, predicate: Callable[[Product], bool]) -> 'ProductCatalog':
        new_catalog = ProductCatalog()
        for item in self._items:
            if predicate(item):
                new_catalog.add(item)
        return new_catalog
    
    def map_to(self, func: Callable[[Product], Any]) -> list:
        return list(map(func, self._items))