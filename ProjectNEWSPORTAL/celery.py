import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')
app = Celery('news')
app.config_from_object('django.conf:settings', name='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.last_post_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': ()
    },

    'action_when_news_create': {
        'task': 'news.tasks.notify_about_new_post_when_create',
        'schedule': crontab(minute=30),
        'args': ()
    },

}
