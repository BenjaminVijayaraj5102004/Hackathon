from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class Supplier(BaseModel):
    supplier_id: int
    supplier_name: str          # varchar(150)
    contact_number: str         # varchar(20)
    email: str                  # varchar(150)
    lead_time_days: int
    address: str                # varchar(255)
    is_active: bool


class PurchaseOrder(BaseModel):
    purchase_order_id: int
    supplier_id: int
    store_id: int
    order_date: datetime
    expected_delivery_date: datetime
    status: str                 # varchar(30)
    total_amount: Decimal       # decimal(10,2)


class PurchaseOrderDetail(BaseModel):
    purchase_order_id: int
    product_id: int
    quantity_ordered: int
    unit_cost: Decimal          # decimal(10,2)
