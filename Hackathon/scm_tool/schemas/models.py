from pydantic import BaseModel, Field
from typing import Optional


# ─── Input Schemas ───────────────────────────────────────────────

class ProcessDayInput(BaseModel):
    demand: int = Field(..., ge=0, description="Customer demand for the day")

class InitStoreInput(BaseModel):
    product: str = Field(default="Biscuit", description="Product name")
    initial_stock: int = Field(default=40, ge=0, description="Opening stock")
    reorder_point: int = Field(default=10, ge=0, description="Stock level that triggers reorder")
    cost_price: float = Field(default=5.0, gt=0, description="Cost price per unit")
    selling_price: float = Field(default=10.0, gt=0, description="Selling price per unit")
    lead_time_days: int = Field(default=2, ge=1, description="Supplier delivery lead time")
    forecast_window: int = Field(default=3, ge=1, description="Moving average window size")


# ─── Output Schemas ──────────────────────────────────────────────

class DayResult(BaseModel):
    day: int
    opening_stock: int
    demand: int
    sold: int
    lost_sales: int
    closing_stock: int
    revenue: float
    cost: float
    profit: float
    total_profit: float
    predicted_next_demand: int
    reorder_placed: bool
    reorder_quantity: Optional[int] = None
    delivery_expected_day: Optional[int] = None
    deliveries_received: list[int] = Field(default_factory=list)

class HolidayResult(BaseModel):
    day: int
    message: str = "Holiday — store closed, day skipped"

class StoreStatus(BaseModel):
    day: int
    product: str
    current_stock: int
    reorder_point: int
    cost_price: float
    selling_price: float
    lead_time_days: int
    total_profit: float
    pending_orders: list[dict]
    forecast_history: list[int]
    predicted_next_demand: int

class SummaryReport(BaseModel):
    total_days_operated: int
    total_profit: float
    total_sales: int
    total_lost_sales: int
    days: list[dict]

class EmptyInput(BaseModel):
    """No parameters required."""
    pass

class ToolError(BaseModel):
    success: bool = False
    error: str
