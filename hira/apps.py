from django.apps import AppConfig


class HiraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hira'

    def ready(self):
        import hira.signals
