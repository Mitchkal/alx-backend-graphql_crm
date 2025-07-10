#!/usr/bin/env python3
"""
uses gql library to query endpoind for
orders with order_date within last 7 days
and logs each order's id and customer email to
tmp/order_reminders_log.txt with timestamp
"""
import logging
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime, timedelta
import os
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file = "/tmp/order_reminders_log.txt"
# Create file handler
# log_file_path = log_file.replace("~", str(Path.home()))
try:
    # Ensure directory exists
    # os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    # Create a file handler
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
except Exception as e:
    print(f"Error setting up logging: {e}")

# Get today's date and calculate the date 7 days ago
seven_days_ago = (datetime.today() - timedelta(days=7)).date()

# select transport with defined url endpont
transport = AIOHTTPTransport(url="http://localhost:8000/graphql")

# create graphql client with defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Create a gql query
query = gql(
    """
    query MyQuery ($sevenDaysAgo: Date!) {
    filteredOrders(orderDate_Gte: $sevenDaysAgo){
    edges {
        node {
         orderDate
         customer {
            email
            name
        }
        id
    }
    }    
    }
}
"""
)
# execute Query on transprt
result = client.execute(
    query, variable_values={"sevenDaysAgo": seven_days_ago.isoformat()}
)

# Log each orders id and customer email
for order in result["filteredOrders"]["edges"]:
    order_node = order["node"]
    order_id = order_node["id"]
    customer_email = order_node["customer"]["email"]
    logger.info(f"Order ID: {order_id}, Customer Email: {customer_email}")
    # , Date: {order_node['orderDate']}

print("Order reminders processed!")
