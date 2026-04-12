from lib.validate import (
    validate_name,
    validate_price,
    validate_discount,
    validate_stock,
    validate_category,
    validate_product_id
)

class Product:
    currency = "₽"

    def __init__(self, name, price, stock, discount, category, product_id):
        self._name = validate_name(name)
        self._price = validate_price(price)
        self._stock = validate_stock(stock)
        self._discount = validate_discount(discount)
        self._category = validate_category(category)      
        self.__product_id = validate_product_id(product_id)
        
        self._active = True
        self.update_available()

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = price

    @property
    def discount(self):
        return self._discount
    
    @discount.setter
    def discount(self, discount):
        self._discount = discount

    @discount.deleter
    def discount(self):
        self._discount = 0

    @property
    def stock(self):
        return self._stock
    
    @stock.setter
    def stock(self, stock):
        self._stock = stock

    @property
    def product_id(self):
        return self.__product_id

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        self._category = category

    @property
    def active(self):
        return self._active

    def get_final_price(self):
        if not self._active:
            raise ValueError("Товар снят с продажи")
        return round(self._price * (100 - self._discount) / 100, 2)

    def update_available(self):
        if self._stock > 0:
            self.activate()
        else:
            self.deactivate()  
    
    def reduce_stock(self, quantity):
        if not self._active:
            raise ValueError("Товар снят с продажи")
        if self._stock < quantity:
            raise ValueError(f"На складе всего {self._stock} шт., а вы хотите {quantity}")
        if quantity <= 0:
            raise ValueError("Количество должно быть больше 0")
        self._stock -= quantity
        self.update_available()
    
    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def calculate_price(self):
        return self.get_final_price()

    def __str__(self):
        return f"{self._name} - {self._price} {self.currency} ({self._stock} шт.)"

    def __repr__(self):
        return (
            f"Product(name={self._name!r}, price={self._price}, stock={self._stock}, "
            f"discount={self._discount}, category={self._category!r}, product_id={self.__product_id!r})"
        )
    
    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.__product_id == other.__product_id
    
    