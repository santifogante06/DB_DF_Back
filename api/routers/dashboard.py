from fastapi import APIRouter
from mysql.connector import MySQLConnection
from backend.db_connection import get_db_connection
from fastapi import Depends
from backend.utils.load_queries import load_queries
from typing import List
from fastapi import HTTPException, status
from fastapi import Query
from fastapi import Path
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
async def product_stock(
    db: MySQLConnection = Depends(get_db_connection),
    name: str | None = Query(default=None, description="Filter by product name"),
    low_stock: bool  = Query(default=False, description="Filter by low stock status"),
    sort_by: str | None = Query(default=None, description="Sort by column"),
    order: str = Query(default="asc", description="Sort order (asc/desc)"),
    limit: int = Query(default=100, description="Limit the number of results"),
    offset: int | None = Query(default=None, description="Offset for pagination")
):
    try:
        cursor = db.cursor(dictionary=True)

        base_query = queries["product_stock"]
        conditions = []
        parameters = []
        if name:
            conditions.append("product_name LIKE %s")
            parameters.append(f"%{name}%")
        if low_stock:
            conditions.append("stock_quantity < 2")
        allowed_sort_columns = ["product_name", "stock_quantity", "product_id"]
        if sort_by in allowed_sort_columns:
            base_query += f" ORDER BY {sort_by} {order.upper() if order in ['asc', 'desc'] else 'ASC'}"
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        if limit:
            base_query += " LIMIT %s"
            parameters.append(limit)
            if offset:
                base_query += " OFFSET %s"
                parameters.append(offset)

        cursor.execute(base_query, parameters)
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
async def location_stock(
    db: MySQLConnection = Depends(get_db_connection),
    name: str | None = Query(default=None, description="Filter by product name"),
    limit: int = Query(default=100, description="Limit the number of results"),
    offset: int | None = Query(default=None, description="Offset for pagination"),
    location: str | None = Query(default=None, description="Filter by location name")
):
    try:
        cursor = db.cursor(dictionary=True)

        base_query = queries["location_stock"]
        conditions = []
        parameters = []
        if name:
            conditions.append("product_name LIKE %s")
            parameters.append(f"%{name}%")
        if location:
            conditions.append("ubicaciones_location LIKE %s")
            parameters.append(f"%{location}%")
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        if limit:
            base_query += " LIMIT %s"
            parameters.append(limit)
            if offset:
                base_query += " OFFSET %s"
                parameters.append(offset)

        cursor.execute(base_query, parameters)
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
async def product_detail(
    db: MySQLConnection = Depends(get_db_connection),
    name: str | None = Query(default=None, description="Filter by product name"),
    limit: int = Query(default=100, description="Limit the number of results"),
    offset: int | None = Query(default=None, description="Offset for pagination"),
    location: str | None = Query(default=None, description="Filter by location name"),
    sort_by: str | None = Query(default=None, description="Sort by column"),
    order: str = Query(default="asc", description="Sort order (asc/desc)")
):
    try:
        cursor = db.cursor(dictionary=True)
        base_query = queries["product_detail"]
        conditions = []
        parameters = []
        if name:
            conditions.append("product_name LIKE %s")
            parameters.append(f"%{name}%")
        if location:
            conditions.append("ubicaciones_location LIKE %s")
            parameters.append(f"%{location}%")
        allowed_sort_columns = ["product_name", "stock_quantity", "ubicaciones_location"]
        if sort_by in allowed_sort_columns:
            base_query += f" ORDER BY {sort_by} {order.upper() if order in ['asc', 'desc'] else 'ASC'}"
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        if limit:
            base_query += " LIMIT %s"
            parameters.append(limit)
            if offset:
                base_query += " OFFSET %s"
                parameters.append(offset)

        cursor.execute(base_query, parameters)
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
async def stock_movement(
    db: MySQLConnection = Depends(get_db_connection),
    name: str | None = Query(default=None, description="Filter by product name"),
    limit: int = Query(default=100, description="Limit the number of results"),
    offset: int | None = Query(default=None, description="Offset for pagination"),
    location: str | None = Query(default=None, description="Filter by location name"),
    sort_by: str | None = Query(default=None, description="Sort by column"),
    order: str = Query(default="asc", description="Sort order (asc/desc)"),
    action: str | None = Query(default=None, description="Filter by action type (e.g., 'insert', 'update')"),
    action_function: str | None = Query(default=None, description="Filter by action function (e.g., 'add', 'remove')"),
    from_date: str | None = Query(default=None, description="Filter from date"),
    to_date: str | None = Query(default=None, description="Filter to date")
):
    try:
        cursor = db.cursor(dictionary=True)
        base_query = queries["stock_movement"]
        conditions = []
        parameters = []
        if name:
            conditions.append("product_name LIKE %s")
            parameters.append(f"%{name}%")
        if location:
            conditions.append("ubicaciones_location LIKE %s")
            parameters.append(f"%{location}%")
        allowed_sort_columns = ["product_name", "stock_quantity", "ubicaciones_location"]
        if sort_by in allowed_sort_columns:
            base_query += f" ORDER BY {sort_by} {order.upper() if order in ['asc', 'desc'] else 'ASC'}"
        if action in ["insert", "update"]:
            conditions.append("action = %s")
            parameters.append(action)
        if action_function in ["add", "remove"]:
            conditions.append("action_function = %s")
            parameters.append(action_function)
        if from_date:
            conditions.append("h.action_date_time >= %s")
            parameters.append(from_date)
        if to_date:
            conditions.append("h.action_date_time <= %s")
            parameters.append(to_date)
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        if limit:
            base_query += " LIMIT %s"
            parameters.append(limit)
            if offset:
                base_query += " OFFSET %s"
                parameters.append(offset)

        cursor.execute(base_query, parameters)
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
async def product_stock_byid(product_id: int = Path(..., gt=0, description="The ID of the product must be greater than 0"), db: MySQLConnection = Depends(get_db_connection)):
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
async def location_stock_byid(ubicaciones_id: int = Path(..., gt=0, description="The ID of the location must be greater than 0"), db: MySQLConnection = Depends(get_db_connection)):
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
async def product_detail_byid(product_id: int = Path(..., gt=0, description="The ID of the product must be greater than 0"), db: MySQLConnection = Depends(get_db_connection)):
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
async def low_stock_alert_byid(product_id: int = Path(..., gt=0, description="The ID of the product must be greater than 0"), db: MySQLConnection = Depends(get_db_connection)):
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
async def stock_movement_byid(product_id: int = Path(..., gt=0, description="The ID of the product must be greater than 0"), db: MySQLConnection = Depends(get_db_connection)):
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

