from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel


class DynamicPricing(BaseModel):
    pricing_id: int
    product_id: int
    store_id: int
    current_price: Decimal          # decimal(10,2)
    suggested_price: Decimal        # decimal(10,2)
    demand_elasticity_score: Decimal  # decimal(6,3)
    suggested_by: str               # varchar(100)
    created_at: datetime


class Promotion(BaseModel):
    promotion_id: int
    product_id: int
    discount_percent: Decimal       # decimal(5,2)
    start_date: date
    end_date: date
    is_active: bool


class SeasonalityPattern(BaseModel):
    pattern_id: int
    product_id: int
    store_id: int
    month: int
    seasonal_index: Decimal         # decimal(6,3)
    year: int


class DailyProductSales(BaseModel):
    id: int
    store_id: int
    product_id: int
    date: date
    total_quantity_sold: int
    total_revenue: Decimal          # decimal(12,2)
