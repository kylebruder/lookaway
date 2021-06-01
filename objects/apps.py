from django.apps import AppConfig


class ObjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'objects'

    def ready(self):
        import objects.signals
