import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quokka_server.settings')

app = Celery('quokka_server')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
