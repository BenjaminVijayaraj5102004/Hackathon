from pydantic import BaseModel


class Warehouse(BaseModel):
    warehouse_id: int
    warehouse_name: str     # varchar(150)
    location: str           # varchar(200)
    capacity: int
    manager_name: str       # varchar(150)
    is_active: bool


class StoreWarehouseMap(BaseModel):
    map_id: int
    store_id: int
    warehouse_id: int
