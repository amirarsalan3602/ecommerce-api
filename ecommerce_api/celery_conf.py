from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault("DJANGO_SETTING_MODEL", 'ecommerce_api.settings')

celery_app = Celery('ecommerce_api')
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'redis://localhost:6379/0'
celery_app.conf.result_backend = 'redis://localhost:6379/0'
celery_app.conf.task_serializers = 'json'
celery_app.conf.result_serializers = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always = False
celery_app.conf.worker_prefetch_multiplier = 4
