from django.apps import AppConfig


class LsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ls'

    def ready(self):
        def ready(self):
            from . import signals