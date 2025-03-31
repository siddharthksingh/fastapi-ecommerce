from pydantic import BaseModel


class Order(BaseModel):
    items: dict[str, int] = {}