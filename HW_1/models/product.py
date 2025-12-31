class Product:
    name: str
    category: str
    price: float
    sale: int

    def __init__(self, name: str, category: str, price: float) -> None:
        self.name = name
        self.category = category
        self.price = price
        self.sale = 0

    def edit_category(self, new_category: str) -> None:
        self.category = new_category

    def edit_price(self, new_price: float) -> None:
        self.price = new_price

    def set_sale(self, sale) -> None:
        self.sale = sale

    def cancel_sale(self) -> None:
        self.sale = 0

    def get_price(self) -> float:
        return self.price - (self.price * self.sale) / 100

    def __repr__(self) -> str:
        return f"Название: {self.name},\nКатегория: {self.category},\nЦена: {self.price},\nСкидка: {self.sale},\nЦена с учетом скидки: {self.get_price()}\n"
