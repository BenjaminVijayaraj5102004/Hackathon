from pydantic import BaseModel


class Store(BaseModel):
    store_id: int
    store_name: str  # varchar(150)
    location: str    # varchar(200)


class Category(BaseModel):
    category_id: int
    category_name: str  # varchar(100)
