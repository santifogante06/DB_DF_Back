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
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, 1 AS min_required
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
WHERE s.stock_quantity <= 1

-- stock_movement
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, l.ubicaciones_location AS ubicaciones_location, h.action AS action, h.action_date_time AS action_date_time, h.action_function AS action_function
FROM products_df p
JOIN stock_df s ON p.product_id = s.product_id
JOIN ubicaciones_df l ON s.ubicaciones_id = l.ubicaciones_id
JOIN history_df h ON p.product_id = h.product_id




