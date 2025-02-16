from django.apps import AppConfig


class ClassroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classroom'

    def ready(self):
        import classroom.signals