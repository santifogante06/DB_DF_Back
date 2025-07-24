from fastapi import APIRouter
from mysql.connector import MySQLConnection
from backend.db_connection import get_db_connection
from fastapi import Depends
from backend.utils.load_queries import load_queries
from typing import List
from fastapi import HTTPException, status
from api.models.models import (
    ProductStock,
    LocationStock,
    ProductDetail,
    LowStockAlert,
    StockMovement,
)

router = APIRouter()

queries = load_queries("api/queries_api.sql")

@router.get("/product-stock", response_model=List[ProductStock])
async def product_stock(db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["product_stock"])
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product stock data found")
        return [ProductStock(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch product stock data: {str(e)}")

@router.get("/location-stock", response_model=List[LocationStock])
async def location_stock(db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["location_stock"])
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No location stock data found")
        return [LocationStock(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch location stock data: {str(e)}")

@router.get("/product-detail", response_model=List[ProductDetail])
async def product_detail(db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["product_detail"])
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product detail data found")
        return [ProductDetail(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch product detail data: {str(e)}")

@router.get("/low-stock-alert", response_model=List[LowStockAlert])
async def low_stock_alert(db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["low_stock_alert"])
        result = cursor.fetchall()
        cursor.close()
        return [LowStockAlert(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch low stock alert data: {str(e)}")

@router.get("/stock-movement", response_model=List[StockMovement])
async def stock_movement(db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["stock_movement"])
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No stock movement data found")
        return [StockMovement(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch movement stock data: {str(e)}")

@router.get("/product-stock-byid/{product_id}", response_model=List[ProductStock])
async def product_stock_byid(product_id: int, db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["product_stock_byid"], (product_id,))
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product stock data found")
        return [ProductStock(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch product stock data: {str(e)}")

@router.get("/location-stock-byid/{ubicaciones_id}", response_model=List[LocationStock])
async def location_stock_byid(ubicaciones_id: int, db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["location_stock_byid"], (ubicaciones_id,))
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No location stock data found")
        return [LocationStock(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch location stock data: {str(e)}")

@router.get("/product-detail-byid/{product_id}", response_model=List[ProductDetail])
async def product_detail_byid(product_id: int, db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["product_detail_byid"], (product_id,))
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product detail data found")
        return [ProductDetail(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch product detail data: {str(e)}")

@router.get("/low-stock-alert-byid/{product_id}", response_model=List[LowStockAlert])
async def low_stock_alert_byid(product_id: int, db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["low_stock_alert_byid"], (product_id,))
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No low stock alert data found")
        return [LowStockAlert(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch low stock alert data: {str(e)}")

@router.get("/stock-movement-byid/{product_id}", response_model=List[StockMovement])
async def stock_movement_byid(product_id: int, db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(queries["stock_movement_byid"], (product_id,))
        result = cursor.fetchall()
        cursor.close()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No stock movement data found")
        return [StockMovement(**row) for row in result]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to fetch stock movement data: {str(e)}")

