from fastapi import APIRouter
from mysql.connector import MySQLConnection
from backend.db_connection import get_db_connection
from fastapi import Depends
from backend.utils.load_queries import load_queries
from models.models import (
    ProductStock,
    LocationStock,
    ProductDetail,
    LowStockAlert,
    StockMovement,
)

router = APIRouter()

@router.get("/test")
async def test():
    return {"message": "Test endpoint funcionando correctamente"}

@router.get("/product-stock", response_model=ProductStock)
async def product_stock(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute(load_queries("product_stock"))
    result = cursor.fetchall()
    cursor.close()
    return {"product-stock": result}

@router.get("/location-stock", response_model=LocationStock)
async def location_stock(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute(load_queries("location_stock"))
    result = cursor.fetchall()
    cursor.close()
    return {"location-stock": result}

@router.get("/product-detail", response_model=ProductDetail)
async def product_detail(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute(load_queries("product_detail"))
    result = cursor.fetchall()
    cursor.close()
    return {"product-detail": result}

@router.get("/low-stock-alert", response_model=LowStockAlert)
async def low_stock_alert(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute(load_queries("low_stock_alert"))
    result = cursor.fetchall()
    cursor.close()
    return {"low-stock-alert": result}

@router.get("/stock-movement", response_model=StockMovement)
async def stock_movement(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute(load_queries("stock_movement"))
    result = cursor.fetchall()
    cursor.close()
    return {"stock-movement": result}
