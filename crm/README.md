steps to:InstallRedis and dependencies.Run migrations (python manage.py migrate).Start Celery worker (celery -A crm worker -l info).Start Celery Beat (celery -A crm beat -l info).Verify logs in /tmp/crm_report_log.txt.

# Install Redis

sudo apt update
sudo apt install redis-server

# Enable and start Redis

sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verify it's running

redis-cli ping # should return: PONG

After adding django_celery_beat to your INSTALLED_APPS:

bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate

. Start the Celery Worker
Run this in your project root (same folder as manage.py):

bash
Copy
Edit
celery -A crm worker -l info

4.  Start Celery Beat Scheduler
    In a separate terminal window:

bash
Copy
Edit
celery -A crm beat -l info

5. Verify the Logs
   After the scheduled task runs (or you can trigger it manually):

bash
Copy
Edit
python manage.py shell
python
Copy
Edit
from crm.tasks import generate_crm_report
generate_crm_report.delay()
Then check:

bash
Copy
Edit
cat /tmp/crm_report_log.txt
You should see:

yaml
Copy
Edit
2025-07-13 14:00:00 - Report: 25 customers, 50 orders, 10000.0 revenue
