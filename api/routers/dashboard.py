from fastapi import APIRouter
from mysql.connector import MySQLConnection
from backend.db_connection import get_db_connection
from fastapi import Depends
from backend.utils.load_queries import load_queries
from typing import List
from api.models.models import (
    ProductStock,
    LocationStock,
    ProductDetail,
    LowStockAlert,
    StockMovement,
)

router = APIRouter()

queries = load_queries("api/queries_api.sql")

@router.get("/test")
async def test():
    return {"message": "Test endpoint funcionando correctamente"}

@router.get("/product-stock", response_model=List[ProductStock])
async def product_stock(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute(queries["product_stock"])
    result = cursor.fetchall()
    cursor.close()
    return [ProductStock(**row) for row in result]

@router.get("/location-stock", response_model=List[LocationStock])
async def location_stock(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute(queries["location_stock"])
    result = cursor.fetchall()
    cursor.close()
    return [LocationStock(**row) for row in result]

@router.get("/product-detail", response_model=List[ProductDetail])
async def product_detail(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute(queries["product_detail"])
    result = cursor.fetchall()
    cursor.close()
    return [ProductDetail(**row) for row in result]

@router.get("/low-stock-alert", response_model=List[LowStockAlert])
async def low_stock_alert(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute(queries["low_stock_alert"])
    result = cursor.fetchall()
    cursor.close()
    return [LowStockAlert(**row) for row in result]

@router.get("/stock-movement", response_model=List[StockMovement])
async def stock_movement(db: MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute(queries["stock_movement"])
    result = cursor.fetchall()
    cursor.close()
    return [StockMovement(**row) for row in result]
