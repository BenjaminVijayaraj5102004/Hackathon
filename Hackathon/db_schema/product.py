from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class Product(BaseModel):
    product_id: int
    product_code: str           # varchar(50), NOT NULL
    product_name: str           # varchar(150)
    category_id: int
    unit_price: Decimal         # decimal(10,2)
    reorder_level: int
    is_active: bool
    created_at: datetime


class Inventory(BaseModel):
    inventory_id: int
    store_id: int
    product_id: int
    quantity_in_stock: int
    last_updated: datetime
