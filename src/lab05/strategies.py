from typing import Callable
from lab03.base import Product
from lab03.models import Perfume, Skincare, Makeup


def by_name(item: Product) -> str:
    return item.name.lower()


def by_price(item: Product) -> float:
    return item.price


def by_stock(item: Product) -> int:
    return item.stock


def by_discount(item: Product) -> int:
    return item.discount


def by_category_then_price(item: Product) -> tuple:
    return (item.category.lower(), item.price)


def is_available(item: Product) -> bool:
    return item.stock > 0


def has_discount(item: Product) -> bool:
    return item.discount > 0


def is_perfume(item: Product) -> bool:
    return isinstance(item, Perfume)


def is_skincare(item: Product) -> bool:
    return isinstance(item, Skincare)


def make_price_filter(max_price: float) -> Callable[[Product], bool]:
    def price_filter(item: Product) -> bool:
        return item.price <= max_price
    return price_filter


def make_stock_filter(min_stock: int) -> Callable[[Product], bool]:
    def stock_filter(item: Product) -> bool:
        return item.stock >= min_stock
    return stock_filter


def is_makeup(item: Product) -> bool:
    return isinstance(item, Makeup)

class DiscountStrategy:
    def __init__(self, percent: float):
        self._percent = percent
    
    def __call__(self, item: Product) -> Product:
        if item.discount < self._percent:
            item.discount = int(self._percent)
        return item


class StatusReportStrategy:
    def __call__(self, item: Product) -> str:
        status = []
        if not item._active:
            status.append("неактивен")
        elif item.stock == 0:
            status.append("нет в наличии")
        else:
            status.append(f"в наличии ({item.stock} шт.)")
        
        if item.discount > 0:
            status.append(f"скидка {item.discount}%")
        
        if isinstance(item, Perfume):
            status.append(f"объём {item.volume}мл")
        elif isinstance(item, Skincare):
            status.append(f"тип кожи: {item.skin_type}")
        elif isinstance(item, Makeup):
            status.append(f"оттенок: {item.shade}")
        
        return f"{item.name}: {', '.join(status)}"