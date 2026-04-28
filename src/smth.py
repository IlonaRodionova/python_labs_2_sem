class Product:
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    def calculate_price(self) -> float:
        return self._price

    def __str__(self):
        return f"{self._name}: {self._price:.2f} руб."

# Ваш код:
class DigitalProduct(Product):
    def __init__(self, name: str, price: float, file_size_mb: int):
        super().__init__(self, name, price)
        self.file_size_mb = file_size_mb

    def calculate_price(self):
        if self.file_size_mb > 100:
            return self.price * 0.90
        return self.price

    def get_info(self):
        return f"[Цифровой] {self.name} {self.file_size_mb} MB"
































