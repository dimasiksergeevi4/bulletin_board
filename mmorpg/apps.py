from django.apps import AppConfig


class MmorpgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mmorpg'

    def ready(self):
        import mmorpg.signals
