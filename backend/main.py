import paho.mqtt.client as mqtt
import json
import mysql.connector
import re
from datetime import datetime
from db_connection import get_db_connection
from backend.utils import load_queries

# Load SQL queries from the file
queries = load_queries("backend/queries.sql")

def on_connect(client, userdata, flags, rc):
    """"Callback function for when the client connects to the MQTT broker."""
    print("Connected with result code " + str(rc) + "\n")
    client.subscribe("BackPy4570/backend")

def on_message(client, userdata, msg):
    """Callback function for when a message is received from the MQTT broker."""
    payload = msg.payload.decode("utf-8")
    # Decoding the payload to a JSON object
    json_document = json.loads(payload)

    if validate_json(json_document):
        # Insert the data into the MySQL database
        try:
            # Check if the product already exists
            check_product_exists = queries["check_product_exists"]
            cursor.execute(check_product_exists, (json_document["products"]["name"], json_document["products"]["barcode"]))
            result = cursor.fetchone()
            if result:
                product_id = result[0]
                commit_for_update(product_id, json_document)
                return
            commit_for_insert(json_document)
        except mysql.connector.Error as err:
            publish_error(mqttc, f"Error inserting data into MySQL: {err}")

def commit_for_update(product_id, json_document):
    """Update the existing product's stock and time in the MySQL database."""
    get_stock_query = queries["get_current_stock"]
    cursor.execute(get_stock_query, (product_id,))
    current_stock = cursor.fetchone()
    new_quantity = current_stock[0]+ json_document["stock"]["quantity"]
    if new_quantity < 0:
        publish_error(mqttc, "Insufficient stock.")
        return
    update_query = queries["stock_update"]
    cursor.execute(update_query, (new_quantity, product_id))
    db.commit()
    publish_success(mqttc, "Stock updated successfully.")
    get_stock_id_query = queries["get_stock_id"]
    cursor.execute(get_stock_id_query, (product_id,))
    stock_id_result = cursor.fetchone()[0]
    update_time_query = queries["update_time"]
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(update_time_query, (current_time, stock_id_result))
    db.commit()
    publish_success(mqttc, "Time updated successfully.")
    action = "update"
    action_function = "add"
    if json_document["stock"]["quantity"] < 0:
        action_function = "remove"
    cursor.execute(queries["set_history"], (product_id, action, action_function))
    db.commit()
    publish_success(mqttc, "History updated successfully.")

def commit_for_insert(json_document):
    """Insert a new product, location, and stock into the MySQL database."""
    if  not negative_stock_validation_insert(json_document["stock"]):
        return
    query_for_products = queries["insert_product"]
    cursor.execute(query_for_products, (json_document["products"]["name"], json_document["products"]["barcode"]))
    db.commit()
    product_id = cursor.lastrowid  # Get the last inserted product ID
    query_for_ubicaciones = queries["insert_locations"]
    cursor.execute(query_for_ubicaciones, (json_document["location"]["column"], json_document["location"]["row"], product_id))
    db.commit()
    ubicaciones_id = cursor.lastrowid  # Get the last inserted ubicaciones ID
    query_for_stock = queries["insert_stock"]
    cursor.execute(query_for_stock, (json_document["stock"]["quantity"], product_id, ubicaciones_id))
    db.commit()
    stock_id = cursor.lastrowid  # Get the last inserted stock ID
    query_for_time_foreignid = queries["insert_time_foreignid"]
    cursor.execute(query_for_time_foreignid, (stock_id,))
    db.commit()
    query_for_history = queries["set_history"]
    action = "insert"
    cursor.execute(query_for_history, (product_id, action, "add"))
    db.commit()
    publish_success(mqttc, "Data inserted successfully into MySQL database.")

def json_validation(json_document):
    """Validate the JSON document structure."""
    object_keys = ["products", "location", "stock"]
    for key in object_keys:
        if key not in json_document:
            publish_error(mqttc, f"Missing required key: {key}")
            return False
    product_keys = ["name", "barcode"]
    for key in product_keys:
        if key not in json_document["products"]:
            publish_error(mqttc, f"Missing required key in products: {key}")
            return False
    location_keys = ["column", "row"]
    for key in location_keys:
        if key not in json_document["location"]:
            publish_error(mqttc, f"Missing required key in location: {key}")
            return False
    stock_keys = ["quantity"]
    for key in stock_keys:
        if key not in json_document["stock"]:
            publish_error(mqttc, f"Missing required key in stock: {key}")
            return False
    # Additional validations
    try:
        if not isinstance(json_document["products"]["name"], str) or json_document["products"]["name"] is None or json_document["products"]["name"].strip() == "":
            publish_error(mqttc, "name must be a non-empty string")
            return False
        if not isinstance(json_document["products"]["barcode"], int):
            publish_error(mqttc, "barcode must be an integer")
            return False
        if not isinstance(json_document["location"]["column"], int):
            publish_error(mqttc, "column must be an integer")
            return False
        if not isinstance(json_document["location"]["row"], str) or json_document["location"]["row"] is None or json_document["location"]["row"].strip() == "":
            publish_error(mqttc, "row must be a non-empty string")
            return False
        if not isinstance(json_document["stock"]["quantity"], int):
            publish_error(mqttc, "quantity must be an integer")
            return False
    except ValueError as e:
        publish_error(mqttc, f"JSON validation error: {e}")
        return False
    return True

def regex_validation(barcode):
    """Validate the barcode using a regular expression."""
    pattern = r"^\d{6,20}$"  # Example pattern for a 6 to 20-digit barcode
    if re.match(pattern, str(barcode)):
        return True
    publish_error(mqttc, "Invalid barcode format.")
    return False

def regex_location_validation(location):
    """Validate the location using a regular expression."""
    pattern = r"^[A-Z]{1,2}\d{1,2}$"  # Example pattern for a location like 'A1', 'B12', etc.
    if re.match(pattern, location["row"] + str(location["column"])):
        return True
    publish_error(mqttc, "Invalid location format.")
    return False

def regex_stock_validation(stock):
    """Validate the stock quantity using a regular expression."""
    pattern = r"^-?\d+$"  # Example pattern for a signed integer (can be negative)
    if re.match(pattern, str(stock["quantity"])):
        return True
    publish_error(mqttc, "Invalid stock quantity format.")
    return False

def negative_stock_validation_insert(stock):
    """Validate that stock quantity is not negative during insert."""
    if stock["quantity"] < 0:
        publish_error(mqttc, "Stock quantity cannot be negative during insert.")
        return False
    return True

def validate_json(json_document):
    """Validate the JSON document structure and content."""
    if not json_validation(json_document):
        return False
    if not all([
        regex_validation(json_document["products"]["barcode"]),
        regex_location_validation(json_document["location"]),
        regex_stock_validation(json_document["stock"])
    ]):
        return False

    return True

def publish_error(client, error_message):
    """Publish an error message to the MQTT broker."""
    error_payload = json.dumps({"error": error_message})
    client.publish("BackPy4570/error", error_payload)
    print(f"Error published: {error_message}")

def publish_success(client, success_message):
    """Publish a success message to the MQTT broker."""
    success_payload = json.dumps({"success": success_message})
    client.publish("BackPy4570/success", success_payload)
    print(f"Success published: {success_message}")

# Create an MQTT client instance and set up the callbacks
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Set up the MySQL connection
connection = get_db_connection()
if connection:
    db = connection
    # Create a cursor object to execute SQL queries
    cursor = db.cursor()
else:
    raise Exception("Failed to connect to the database.")

mqttc.connect("test.mosquitto.org", 1883, 60)

mqttc.loop_start()

# Disconnect from the MQTT broker when the user presses 'd'
disconnect = input("Press 'd' to disconnect... \n")

if disconnect == "d":
    mqttc.loop_stop()
    mqttc.disconnect()
    print("Disconnected from MQTT broker.")

