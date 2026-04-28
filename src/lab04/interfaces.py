from abc import ABC, abstractmethod


class PriceCalculable(ABC):
    """Интерфейс для объектов, у которых можно рассчитать цену"""
    
    @abstractmethod
    def calculate_price(self):
        """Рассчитывает итоговую цену с учетом всех факторов"""
        pass


class Displayable(ABC):
    """Интерфейс для объектов, которые можно отобразить"""
    
    @abstractmethod
    def get_display_info(self):
        """Возвращает краткую информацию для отображения"""
        pass


class Discountable(ABC):
    """Интерфейс для объектов, у которых есть скидка"""
    
    @abstractmethod
    def get_discount_percent(self):
        """Возвращает процент скидки"""
        pass
    
    @abstractmethod
    def apply_discount(self):
        """Применяет скидку к цене"""
        pass