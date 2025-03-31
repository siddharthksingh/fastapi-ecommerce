from pydantic import BaseModel


class Product(BaseModel):
    name: str
    cost: float
    quantity: int

class ProductUpdate(BaseModel):
    name: str | None = None
    cost: float | None = None
    quantity: int | None = None