from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel


class DemandForecast(BaseModel):
    forecast_id: int
    product_id: int
    store_id: int
    forecast_date: date
    predicted_demand: int
    model_version: str          # varchar(50)
    confidence_score: Decimal   # decimal(5,2)
    created_at: datetime


class DemandAnomaly(BaseModel):
    anomaly_id: int
    product_id: int
    store_id: int
    sale_id: int
    detected_date: datetime
    detected_quantity: int
    normal_average: int
    is_bulk_order: bool
    agent_remark: str           # varchar(255)


class ReorderRecommendation(BaseModel):
    recommendation_id: int
    product_id: int
    store_id: int
    current_stock: int
    predicted_demand: int
    recommended_quantity: int
    safety_stock: int
    status: str                 # varchar(30)
    generated_by: str           # varchar(180)
    generated_at: datetime


class DemandEvent(BaseModel):
    event_id: int
    event_name: str             # varchar(150)
    start_date: date
    end_date: date
    expected_demand_increase: Decimal  # decimal(5,2)
    region: str                 # varchar(100)


class ForecastAccuracy(BaseModel):
    accuracy_id: int
    product_id: int
    store_id: int
    forecast_date: date
    predicted_demand: int
    actual_demand: int
    error: Decimal              # decimal(10,2)
    rmse: Decimal               # decimal(10,2)
    mape: Decimal               # decimal(10,2)
