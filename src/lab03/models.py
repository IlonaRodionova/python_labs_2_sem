from lab03.base import Product


class Perfume(Product):
    """Парфюм (объем и аромат)"""
    
    def __init__(self, name, price, stock, discount, category, product_id, volume, fragrance_type):
        super().__init__(name, price, stock, discount, category, product_id)
        self._volume = volume
        self._fragrance_type = fragrance_type
    
    @property
    def volume(self):
        return self._volume
    
    @property
    def fragrance_type(self):
        return self._fragrance_type
    
    def get_price_per_ml(self):
        if self._volume > 0:
            return round(self._price / self._volume, 2)
        return 0
    
    def calculate_price(self):
        final_price = super().calculate_price()
        if self._volume >= 100:
            return final_price * 0.95
        return final_price
    
    def __str__(self):
        return f"{self._name} - {self._price} {self.currency} ({self._volume}мл, {self._fragrance_type}) [{self._stock} шт.]"


class Skincare(Product):
    """Уход за кожей (тип кожи и активный компонент)"""
    
    def __init__(self, name, price, stock, discount, category, product_id, skin_type, active_ingredient):
        super().__init__(name, price, stock, discount, category, product_id)
        self._skin_type = skin_type
        self._active_ingredient = active_ingredient
    
    @property
    def skin_type(self):
        return self._skin_type
    
    @property
    def active_ingredient(self):
        return self._active_ingredient
    
    def get_skin_compatibility(self):
        compatibility = {
            "сухая": "отлично подходит",
            "жирная": "хорошо подходит",
            "нормальная": "подходит",
            "комбинированная": "хорошо подходит"
        }
        return compatibility.get(self._skin_type.lower(), "подходит")
    
    def calculate_price(self):
        final_price = super().calculate_price()
        if self._active_ingredient.lower() in ["гиалуроновая кислота", "ретинол", "витамин с"]:
            return final_price * 1.1
        return final_price
    
    def __str__(self):
        return f"{self._name} - {self._price} {self.currency} (для {self._skin_type} кожи, {self._active_ingredient}) [{self._stock} шт.]"


class Makeup(Product):
    """Макияж (оттенок и текстура)"""
    
    def __init__(self, name, price, stock, discount, category, product_id, shade, texture):
        super().__init__(name, price, stock, discount, category, product_id)
        self._shade = shade
        self._texture = texture
    
    @property
    def shade(self):
        return self._shade
    
    @property
    def texture(self):
        return self._texture
    
    def is_limited_edition(self):
        limited_keywords = ["limited", "лимит", "коллекция"]
        return any(keyword in self._name.lower() for keyword in limited_keywords)
    
    def calculate_price(self):
        final_price = super().calculate_price()
        if self.is_limited_edition():
            return final_price * 1.2
        return final_price
    
    def __str__(self):
        return f"{self._name} - {self._price} {self.currency} (оттенок: {self._shade}, {self._texture}) [{self._stock} шт.]"