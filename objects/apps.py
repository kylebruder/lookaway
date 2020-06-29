from django.apps import AppConfig


class ObjectsConfig(AppConfig):
    name = 'objects'

    def ready(self):
        print("Importing signals for Objects app")
        import objects.signals
