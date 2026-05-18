"""
Сохранение и загрузка коллекции в JSON-файл.
"""

import json
from typing import List
from lab03.base import Product
from lab03.models import Perfume, Skincare, Makeup


def serialize_product(product: Product) -> dict:
    """
    Преобразует объект Product в словарь для JSON.
    
    Args:
        product: объект товара
    
    Returns:
        словарь с данными товара
    """
    data = {
        "type": product.__class__.__name__,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
        "discount": product.discount,
        "category": product.category,
        "product_id": product.product_id
    }
    
    if isinstance(product, Perfume):
        data["volume"] = product.volume
        data["fragrance_type"] = product.fragrance_type
    elif isinstance(product, Skincare):
        data["skin_type"] = product.skin_type
        data["active_ingredient"] = product.active_ingredient
    elif isinstance(product, Makeup):
        data["shade"] = product.shade
        data["texture"] = product.texture
    
    return data


def deserialize_product(data: dict) -> Product:
    """
    Восстанавливает объект Product из словаря.
    
    Args:
        data: словарь с данными товара
    
    Returns:
        объект Product (Perfume, Skincare или Makeup)
    
    Raises:
        ValueError: если тип товара неизвестен
    """
    product_type = data.get("type")
    
    if product_type == "Perfume":
        return Perfume(
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            discount=data["discount"],
            category=data["category"],
            product_id=data["product_id"],
            volume=data["volume"],
            fragrance_type=data["fragrance_type"]
        )
    elif product_type == "Skincare":
        return Skincare(
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            discount=data["discount"],
            category=data["category"],
            product_id=data["product_id"],
            skin_type=data["skin_type"],
            active_ingredient=data["active_ingredient"]
        )
    elif product_type == "Makeup":
        return Makeup(
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            discount=data["discount"],
            category=data["category"],
            product_id=data["product_id"],
            shade=data["shade"],
            texture=data["texture"]
        )
    else:
        return Product(
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            discount=data["discount"],
            category=data["category"],
            product_id=data["product_id"]
        )


def save(collection: List[Product], filepath: str) -> None:
    """
    Сохраняет коллекцию товаров в JSON-файл.
    
    Args:
        collection: список товаров
        filepath: путь к файлу
    """
    data = [serialize_product(item) for item in collection]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load(filepath: str) -> List[Product]:
    """
    Загружает коллекцию товаров из JSON-файла.
    
    Args:
        filepath: путь к файлу
    
    Returns:
        список товаров
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [deserialize_product(item) for item in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []