from pydantic import BaseModel
from datetime import datetime

class ProductStock(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int

class LocationStock(BaseModel):
    ubicaciones_id: int
    ubicaciones_location: str
    stock_quantity: int

class ProductDetail(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int
    ubicaciones_location: str

class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int
    min_required: int # Fixed value

class StockMovement(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int
    ubicaciones_location: str
    action: str
    action_function: str
    action_date_time: datetime
