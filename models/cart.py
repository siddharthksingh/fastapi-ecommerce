from pydantic import BaseModel
from models.product import Product

class Cart(BaseModel):
    cartID: int
    items: list[Product]