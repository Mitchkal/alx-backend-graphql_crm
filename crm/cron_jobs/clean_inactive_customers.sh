#!/bin/bash
# executes  python
# command to delete
# customers with no order 
# since a year ago
# and log the count of deleted customers
# cwd
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR/../.." || exit

if [-f "myenv/bin/activate"]; then
    source myenv/bin/activate
else
    echo "Virtual environment not found. Please create it first."
    exit 1
fi
# calculate date one year ago
DATE_THRESHOLD=$(date -d "1 year ago" +%Y-%m-%d)

# Run django shell command to delete inactive customers
DELETED_COUNT=$(echo "
from crm.models import Customer, Order
from django.utils import timezone
from datetime import datetime

date_threshold = datetime.strptime('$DATE_THRESHOLD', '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
customers = Customer.objects.filter(order__isnull=True) | Customer.objects.filter(order__order_date__lt=date_threshold)
count = customers.count()
customers.delete()
print(count)
" | ~/alx-backend-graphql_crm/myenv/bin/python ~/alx-backend-graphql_crm/manage.py shell --no-startup 2>/dev/null | tail -n 1)

echo "$(date '+%Y-%m-%d %H:%M:%S %Z') - Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
