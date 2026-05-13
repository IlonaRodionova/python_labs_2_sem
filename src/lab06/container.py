from typing import TypeVar, Generic, Callable, Optional, Protocol
from lab03.base import Product
from lab03.models import Perfume, Skincare, Makeup

class Displayable(Protocol):
    def display(self) -> str:
        """должен возвращать строку с информацией о товаре"""
        pass


class Scorable(Protocol):
    def score(self) -> float:
        """должен возвращать число (цена, рейтинг и т.д.)"""
        pass

T = TypeVar('T')
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)
R = TypeVar('R')


class TypedCollection(Generic[T]):
    """обобщённая коллекция, ктр хранит элементы одного типа"""
    
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
    
    def remove(self, item: T) -> None:
        if item not in self._items:
            raise ValueError("Элемент не найден")
        self._items.remove(item)
    
    def remove_at(self, index: int) -> T:
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        return self._items.pop(index)
    
    def get_all(self) -> list[T]:
        return self._items.copy()
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        return self._items[index]
    

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> list[R]:
        return [transform(item) for item in self._items]


def add_protocol_methods():
    """добавляем методы в существующие классы для поддержки Protocol"""
    
    # Для Product
    if not hasattr(Product, 'display'):
        def product_display(self):
            try:
                price = self.calculate_price()
                return f"{self.name}: {price} {self.currency} (в наличии: {self.stock})"
            except ValueError:
                return f"{self.name}: недоступен"
        Product.display = product_display
    
    if not hasattr(Product, 'score'):
        def product_score(self):
            try:
                return self.calculate_price()
            except ValueError:
                return 0.0
        Product.score = product_score
    
    # Для Perfume
    if not hasattr(Perfume, 'display'):
        def perfume_display(self):
            try:
                price = self.calculate_price()
                return f"{self.name} | {self.volume}мл | {self.fragrance_type}: {price} {self.currency}"
            except ValueError:
                return f"{self.name}: недоступен"
        Perfume.display = perfume_display
    
    # Для Skincare
    if not hasattr(Skincare, 'display'):
        def skincare_display(self):
            try:
                price = self.calculate_price()
                return f"{self.name} | для {self.skin_type} | {self.active_ingredient}: {price} {self.currency}"
            except ValueError:
                return f"{self.name}: недоступен"
        Skincare.display = skincare_display
    
    # Для Makeup
    if not hasattr(Makeup, 'display'):
        def makeup_display(self):
            try:
                price = self.calculate_price()
                return f"{self.name} | {self.shade} | {self.texture}: {price} {self.currency}"
            except ValueError:
                return f"{self.name}: недоступен"
        Makeup.display = makeup_display


add_protocol_methods()