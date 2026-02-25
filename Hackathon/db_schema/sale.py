from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class Sale(BaseModel):
    sale_id: int
    store_id: int
    customer_id: int
    sale_date: datetime
    total_amount: Decimal       # decimal(10,2)
    payment_method: str         # varchar(50)


class SaleDetail(BaseModel):
    sale_id: int
    product_id: int
    quantity_sold: int
    price_at_sale: Decimal      # decimal(10,2)


class Customer(BaseModel):
    customer_id: int
    name: str                   # varchar(150)
    phone: str                  # varchar(20)
    email: str                  # varchar(150)
    loyalty_points: int
    created_at: datetime
