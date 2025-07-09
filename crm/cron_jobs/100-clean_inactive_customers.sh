#!/bin/bash
# executes  python
# command to delete
# customers with no order 
# since a year ago

# calculate date one year ago
DATE_THRESHOLD=$(date -d "1 year ago" +%Y-%m-%d)

# Run django shell command to delete inactive customers
echo "
from crm.models import Customer, Order
from django.utils import timezone
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file_path =os.path.join(os.path.dirname(__file__), 'customer_cleanup_crontab.txt')
try:
    handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
except Exception as e:
    print(f'Error setting up file logger: {e}')

date_threshold = datetime.strptime('$DATE_THRESHOLD', '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
customers = Customer.objects.filter(order__isnull=True) | Customer.objects.filter(order__order_date__lt=date_threshold)
count = customers.count()
customers.delete()
print(count)
logger.info(f'Deleted {count} inactive customers')
" | ~/alx-backend-graphql_crm/myenv/bin/python ~/alx-backend-graphql_crm/manage.py shell
# 2>/dev/null
