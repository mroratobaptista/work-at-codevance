import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'work_at_codevance.settings')

app = Celery('work_at_codevance')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from work_at_codevance.base.tasks import check_payments_due_today
    sender.add_periodic_task(crontab(hour=0, minute=0), check_payments_due_today.s())


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
