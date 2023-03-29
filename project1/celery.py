from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')



app = Celery("project1")
app.conf.beat_schedule = {
    'scheduled-mail':{
        'task':'project1.app1.tasks.scheduled_mail',
        'schedule': crontab(minute = 2)


    }
}
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()
