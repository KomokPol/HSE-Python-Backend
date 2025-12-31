from typing import List

from models.product import Product


def extract_prices(products: List[Product]) -> List[float]:
    arr_prices = []
    for product in products:
        arr_prices.append(product.get_price())
    return arr_prices
