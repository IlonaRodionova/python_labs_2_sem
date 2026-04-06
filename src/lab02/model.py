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

    # ===== name =====
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    # ===== price =====
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
            self._price = price

    # ===== discount =====
    @property
    def discount(self):
        return self._discount
    
    @discount.setter
    def discount(self, discount):
        self._discount = discount

    @discount.deleter
    def discount(self):
        self._discount = 0

    # ===== stock =====
    @property
    def stock(self):
        return self._stock
    
    @stock.setter
    def stock(self, stock):
        self._stock = stock

    # ===== product_id =====
    @property
    def product_id(self):
        return self.__product_id

    # ===== category =====
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        self._category = category

    # ===== business logic =====
    def get_final_price(self) -> float:
        """ возвращает цену с учетом скидки """
        if not self._active:
            raise ValueError("Товар снят с продажи")
        return round(self._price * (100 - self._discount) / 100, 2)

    def update_available(self) -> None:
        """ проверяет, есть ли товар в наличии """
        if self._stock > 0:
            self.activate()
        else:
            self.deactivate()  
    
    def reduce_stock(self, quantity) -> None:
        """ уменьшает количество товара на складе """
        if not self._active:
            raise ValueError("Товар снят с продажи")
        if self._stock < quantity:
            raise ValueError(f"На складе всего {self._stock} шт., а вы хотите {quantity}")
        if quantity <= 0:
            raise ValueError("Количество должно быть больше 0")
        self._stock -= quantity
        self.update_available()
    
    def activate(self) -> None:
        """ Товар выставлен на продажу """
        self._active = True

    def deactivate(self) -> None:
        """ Товар снят с продажи """
        self._active = False

    # ===== magic =====
    def __str__(self) -> str:
        """ строковое представление товара """
        return f"{self._name} - {self._price} {self.currency} ({self._stock} шт.)"

    def __repr__(self) -> str:
        """ техническое представление для отладки """
        return (
            f"Product(name={self._name!r}, price={self._price}, stock={self._stock}, "
            f"discount={self._discount}, category={self._category!r}, product_id={self.__product_id!r})"
        )
    
    def __eq__(self, other) -> bool:
        """ сравнение товара по product_id """
        if not isinstance(other, Product):
            return False

        return self.__product_id == other.__product_id
    
    def __lt__(self, other) -> bool:
        """ сравнение по цене """
        if not isinstance(other, Product):
            return NotImplemented
        return self._price < other.price 
 
