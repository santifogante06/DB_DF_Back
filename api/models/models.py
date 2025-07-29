from pydantic import BaseModel, Field
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

class StockMovement(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int
    ubicaciones_location: str
    action: str
    action_function: str
    action_date_time: datetime

class ProductData(BaseModel):
    product_name: str
    product_barcode: int

class LocationData(BaseModel):
    ubicaciones_row: str
    ubicaciones_column: int

class StockData(BaseModel):
    stock_quantity: int

class InsertProduct(BaseModel):
    product: ProductData
    location: LocationData
    stock: StockData

class updateProduct(BaseModel):
    product_id: int
    ubicaciones_id: int
    stock: StockData
