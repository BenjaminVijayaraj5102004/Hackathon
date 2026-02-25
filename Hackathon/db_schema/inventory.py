from datetime import datetime
from pydantic import BaseModel


class StockMovement(BaseModel):
    movement_id: int
    product_id: int
    store_id: int
    movement_type: str          # varchar(30)
    quantity_change: int
    reference_id: int
    movement_date: datetime


class InventoryPolicy(BaseModel):
    policy_id: int
    product_id: int
    store_id: int
    safety_stock: int
    reorder_point: int
    max_stock_level: int
    lead_time_days: int


class InventoryLoss(BaseModel):
    loss_id: int
    product_id: int
    store_id: int
    quantity_lost: int
    reason: str                 # varchar(100)
    loss_date: datetime


class StockTransfer(BaseModel):
    transfer_id: int
    from_store_id: int
    to_store_id: int
    product_id: int
    quantity: int
    transfer_date: datetime
    status: str                 # varchar(30)


class ProductBatch(BaseModel):
    batch_id: int
    product_id: int
    store_id: int
    manufacturing_date: str     # date
    expiry_date: str            # date
    quantity_remaining: int


class InventoryRiskAssessment(BaseModel):
    risk_id: int
    product_id: int
    store_id: int
    risk_type: str              # varchar(50)
    risk_score: int
    recommended_action: str     # varchar(255)
    generated_at: datetime
