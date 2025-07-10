#!/usr/bin/env python3
"""
logs message that CRM is alive to
/tmp/crm_heartbeat_log.txt
"""
import logging
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


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

    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")

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


if __name__ == "__main__":
    log_crm_heartbeat()
    print("CRM heartbeat logged successfully!")
