from django.apps import AppConfig


class BootConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boot'

    def ready(self):
        from . import models