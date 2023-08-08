from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')


app = Celery("project1")
app.conf.beat_schedule = {
    'scheduled-mail':{
        'task':'project1.app1.tasks.scheduled_mail',
        'schedule': crontab(minute = 2)
    },

    'scheduled-birthday':{
        'task': 'project1.app1.scheduled_tasks.check_birthday',
        'schedule': crontab(hour = 24)
    }

}
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, related_name='scheduled_tasks')


