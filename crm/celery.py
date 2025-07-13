from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

app = Celery("crm")

# configure Celery with Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# auto-discover tasks in installed apps
app.autodiscover_tasks()
