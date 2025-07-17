-- check_product_exists
SELECT product_id FROM products_df WHERE product_name=%s AND product_barcode=%s;

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

-- stock_update
UPDATE stock_df SET stock_quantity=%s WHERE product_id=%s

-- get_current_stock
SELECT stock_quantity FROM stock_df WHERE product_id=%s;

-- update_time
UPDATE time_df SET date_time=%s WHERE stock_id=%s;

-- get_stock_id
SELECT stock_id FROM stock_df WHERE product_id=%s;

-- set_history
INSERT INTO history_df (product_id, action)
VALUES (%s, %s);