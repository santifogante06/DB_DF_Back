-- insert_product
INSERT INTO products_df (product_name, product_barcode)
VALUES (%s, %s);

-- insert_locations
INSERT INTO ubicaciones_df (ubicaciones_column, ubicaciones_row, product_id)
VALUES (%s, %s, %s);

-- insert_stock
INSERT INTO stock_df (stock_quantity, product_id, ubicaciones_id)
VALUES (%s, %s, %s);

-- insert_time_foreignid
INSERT INTO time_df (stock_id)
VALUES (%s);