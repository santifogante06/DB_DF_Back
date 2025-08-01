-- product_stock
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id

-- location_stock
SELECT l.ubicaciones_id, l.ubicaciones_location, s.stock_quantity AS stock_quantity
FROM ubicaciones_df l
JOIN stock_df s ON l.ubicaciones_id = s.ubicaciones_id

-- product_detail
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, l.ubicaciones_location AS ubicaciones_location
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
JOIN ubicaciones_df l ON s.ubicaciones_id = l.ubicaciones_id

-- low_stock_alert
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
WHERE s.stock_quantity <= 1

-- stock_movement
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, l.ubicaciones_location AS ubicaciones_location, h.action AS action, h.action_date_time AS action_date_time, h.action_function AS action_function
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
JOIN ubicaciones_df l ON s.ubicaciones_id = l.ubicaciones_id
JOIN history_df h ON p.product_id = h.product_id

-- product_stock_byid
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
WHERE p.product_id = %s

-- location_stock_byid
SELECT l.ubicaciones_id, l.ubicaciones_location, s.stock_quantity AS stock_quantity
FROM ubicaciones_df l
JOIN stock_df s ON l.ubicaciones_id = s.ubicaciones_id
WHERE l.ubicaciones_id = %s

-- product_detail_byid
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, l.ubicaciones_location AS ubicaciones_location
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
JOIN ubicaciones_df l ON s.ubicaciones_id = l.ubicaciones_id
WHERE p.product_id = %s

-- low_stock_alert_byid
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
WHERE s.stock_quantity <= 1 AND p.product_id = %s

-- stock_movement_byid
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, l.ubicaciones_location AS ubicaciones_location, h.action AS action, h.action_date_time AS action_date_time, h.action_function AS action_function
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
JOIN ubicaciones_df l ON s.ubicaciones_id = l.ubicaciones_id
JOIN history_df h ON p.product_id = h.product_id
WHERE p.product_id = %s

-- insert_product
INSERT INTO products_df (product_name, product_barcode)
VALUES (%s, %s);

-- insert_locations
INSERT INTO ubicaciones_df (ubicaciones_column, ubicaciones_row)
VALUES (%s, %s);

-- insert_stock
INSERT INTO stock_df (stock_quantity, product_id, ubicaciones_id)
VALUES (%s, %s, %s);

-- insert_time_foreignid
INSERT INTO time_df (stock_id)
VALUES (%s);

-- set_history
INSERT INTO history_df (product_id, action, action_function)
VALUES (%s, %s, %s);

-- check_product_exists
SELECT product_id FROM products_df WHERE product_id = %s;

-- stock_update
UPDATE stock_df SET stock_quantity=%s WHERE product_id=%s

-- get_current_stock
SELECT stock_quantity FROM stock_df WHERE product_id=%s;

-- update_time
UPDATE time_df SET date_time=%s WHERE stock_id=%s;

-- get_stock_id
SELECT stock_id FROM stock_df WHERE product_id=%s;
