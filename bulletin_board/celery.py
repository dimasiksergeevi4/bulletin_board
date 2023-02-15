from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin_board.settings')

app = Celery('bulletin_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'inform_for_new_posts': {
        'task': 'MMORPG_messages.tasks.inform_for_new_posts',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}
