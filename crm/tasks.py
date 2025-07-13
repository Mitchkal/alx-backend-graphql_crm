from celery import shared_task
from django.utils import timezone
import os

from crm.schema import schema  # Adjust import if schema lives elsewhere


@shared_task
def generate_crm_report():
    query = """
    query {
        allCustomers {
            totalCount
        }
        allOrders {
            totalCount
            totalRevenue
        }
    }
    """

    result = schema.execute(query)
    if result.errors:
        log_text = f"{timezone.now()} - Failed to fetch data: {result.errors}\n"
    else:
        customers = result.data["allCustomers"]["totalCount"]
        orders = result.data["allOrders"]["totalCount"]
        revenue = result.data["allOrders"]["totalRevenue"]
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log_text)
