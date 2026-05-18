"""
Собственные исключения для предметной области.
"""


class ItemNotFoundError(Exception):
    """Товар не найден в коллекции."""
    pass


class DuplicateItemError(Exception):
    """Товар с таким идентификатором уже существует."""
    pass


class InvalidDataError(Exception):
    """Некорректные данные при вводе."""
    pass