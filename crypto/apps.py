from django.apps import AppConfig


class CryptoConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'crypto'

    def ready(self):
        import crypto.signals
