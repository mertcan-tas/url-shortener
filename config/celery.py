import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'sync-all-visit-counts-hourly': {
        'task': 'api.tasks.sync_all_visit_counts',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'cleanup-expired-locks-daily': {
        'task': 'api.tasks.cleanup_expired_locks',
        'schedule': crontab(minute=0, hour=0),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
