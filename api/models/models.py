from pydantic import BaseModel

class ProductStock(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int

class LocationStock(BaseModel):
    location_id: int
    location: str
    stock_quantity: int

class ProductDetail(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int
    location: str

class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int
    min_required: int # Fixed value

class StockMovement(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    location: str
    action: str
    function: str
    date_time: str
