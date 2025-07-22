-- product_stock
FROM products_df p
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity
JOIN stock_df s ON p.product_id = s.product_id

-- location_stock
FROM locations_df l
SELECT l.ubicaciones_id, l.ubicaciones_location, s.stock_quantity AS stock_quantity
JOIN stock_df s ON l.location_id = s.location_id

-- product_detail
FROM products_df p
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, l.ubicaciones_location AS location
JOIN stock_df s ON p.product_id = s.product_id
JOIN locations_df l ON s.location_id = l.location_id

-- low_stock_alert
FROM products_df p
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, 1 AS min_required
JOIN stock_df s ON p.product_id = s.product_id
WHERE s.stock_quantity < 1

-- stock_movement
FROM products_df p
SELECT p.product_id, p.product_name, s.stock_quantity AS stock_quantity, l.ubicaciones_location AS location, h.action AS action, h.date_time AS date_time, h.action_function AS function
JOIN stock_df s ON p.product_id = s.product_id
JOIN locations_df l ON s.location_id = l.location_id
JOIN history_df h ON p.product_id = h.product_id




