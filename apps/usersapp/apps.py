from django.apps import AppConfig


class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usersapp'
    label = 'userapp'

    def ready(self):
        import apps.usersapp.signals