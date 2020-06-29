from django.apps import AppConfig


class MembersConfig(AppConfig):
    name = 'members'

    def ready(self):
        print("Importing signals for Members app")
        import members.signals
