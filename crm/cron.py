#!/usr/bin/env python3
"""
logs message that CRM is alive to
/tmp/crm_heartbeat_log.txt
"""
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """
    Logs a heartbeat message to the CRM log file.
    """

    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    log_file = "/tmp/crm_heartbeat_log.txt"

    # Create file handler
    if not logger.handlers:
        try:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s %(message)s", datefmt="%d/%m/%Y-%H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        except Exception as e:
            print(f"Error setting up logging: {e}")
    # Define transport with graphql endpoint

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    # Create graphql client with defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Create a gql query
    query = gql(
        """
        query MyQuery {
        hello
    }
    """
    )
    try:
        result = client.execute(query)
        if result.get("hello") == "Hello, GraphQl!":
            logger.info("CRM is alive")
        else:
            logger.error("CRM is not responding as expected")
    except Exception as e:
        logger.error(f"CRM heartbeat check failed: {e}")

    for handler in logger.handlers:
        handler.flush()
        handler.close()


def update_low_stock():
    """
    executes UpdateLowStockProducts mutation and logs updated product names and new
    stock levels to /tmp/low_stock_updates_log.txt
    """
    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    log_file = "/tmp/low_stock_products_updates_log.txt"

    if not logger.handlers:
        try:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s $(message)s", datefmt="%d/%m/%Y-%H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        except Exception as e:
            print(f"Error setting up logging: {e}")
    # Define transport with graphql endpoiint
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    # creat client
    client = Client(transport=transport)
    query = gql(
        """
        mutation UpdateLowStockProducts {
            updateLowStockProducts {
                productName
                newStockLevel
                success
                message
            }
        }
       """
    )
    result = client.execute(query)
    updates = result.get("updateLowStockProducts", [])
    if updates:
        for update in updates:
            product_name = update.get("productName")
            new_stock_level = update.get("newStockLevel")
            logger.info(f"Product: {product_name}, New Stock Level: {new_stock_level}")
    else:
        logger.info("No low stock products found or updates.")

    for handler in logger.handlers:
        handler.flush()
        handler.close()


if __name__ == "__main__":
    log_crm_heartbeat()
    print("CRM heartbeat logged successfully!")
    update_low_stock()
    print("Low stock products updates logged successfully!")
