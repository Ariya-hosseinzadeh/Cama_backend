from django.apps import AppConfig


class UserCustomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_custom'

    def ready(self):
        import user_custom.signals