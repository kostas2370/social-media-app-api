from django.apps import AppConfig
from django.db.models.signals import post_save


class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app1'

