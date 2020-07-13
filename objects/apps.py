from django.apps import AppConfig


class ObjectsConfig(AppConfig):
    name = 'objects'

    def ready(self):
        import objects.signals
