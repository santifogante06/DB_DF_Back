from fastapi import APIRouter
from mysql.connector import MySQLConnection
from api.utils.db_connection import get_db_connection
from fastapi import Depends
from api.utils.load_queries import load_queries
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from fastapi import Query
from fastapi import Path
from api.models.models import (
    ProductStock,
    LocationStock,
    ProductDetail,
    LowStockAlert,
    StockMovement,
    InsertProduct,
    updateProduct
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
        allowed_sort_columns = ["product_name", "stock_quantity", "action", "action_function", "action_date_time"]
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

@router.post("/insert-product", response_model=InsertProduct)
async def insert_product(product: InsertProduct, db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        db.start_transaction()
        # Insert new product, location, and stock
        # Insert product data
        cursor.execute(queries["insert_product"], (product.product.product_name, product.product.product_barcode))
        product_id = cursor.lastrowid  # Get the last inserted product ID
        # Insert location data
        cursor.execute(queries["insert_locations"], (product.location.ubicaciones_column, product.location.ubicaciones_row))
        ubicaciones_id = cursor.lastrowid  # Get the last inserted ubicaciones ID
        # Insert stock data
        cursor.execute(queries["insert_stock"], (product.stock.stock_quantity, product_id, ubicaciones_id))
        stock_id = cursor.lastrowid  # Get the last inserted stock ID
        # Insert time data
        cursor.execute(queries["insert_time_foreignid"], (stock_id,))
        # Set history
        cursor.execute(queries["set_history"], (product_id, "insert", "add"))
        db.commit()
        cursor.close()
        return product
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to insert product data: {str(e)}")

@router.put("/update-product", response_model=List[updateProduct])
async def update_product(product: updateProduct, db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        db.start_transaction()
        # Check if product exists
        cursor.execute(queries["check_product_exists"], (product.product_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        # Get stock data
        cursor.execute(queries["get_current_stock"], (product.product_id,))
        current_stock = cursor.fetchone()
        if not current_stock:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current stock not found")
        new_quantity = current_stock[0] + product.stock.stock_quantity
        if new_quantity < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
        # Update stock data
        cursor.execute(queries["stock_update"], (new_quantity, product.product_id))
        
        # Set history
        action_function = "add" if product.stock.stock_quantity >= 0 else "remove"
        cursor.execute(queries["set_history"], (product.product_id, "update", action_function))
        
        db.commit()
        cursor.close()
        return [product]
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to update product data: {str(e)}")
    
@router.delete("/delete-product/{product_id}")
async def delete_product(product_id: int = Path(..., gt=0, description="The ID of the product must be greater than 0"), db: MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        db.start_transaction()
        # Check if product exists
        cursor.execute(queries["check_product_exists"], (product_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        # Delete stock data
        cursor.execute(queries["get_stock_id"], (product_id,))
        stock_id = cursor.fetchone()
        if stock_id:
            cursor.execute(queries["delete_time"], (stock_id[0],))
        # Delete stock data
        cursor.execute(queries["get_ubicaciones_id"], (product_id,))
        ubicaciones_id = cursor.fetchone()
        cursor.execute(queries["delete_stock"], (product_id,))
        # Delete location data
        if ubicaciones_id:
            cursor.execute(queries["delete_ubicaciones"], (ubicaciones_id[0],))
        # Set history
        cursor.execute(queries["set_history"], (product_id, "delete", "remove"))

        db.commit()
        cursor.close()
        return {"message": "Product deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error trying to delete product data: {str(e)}")