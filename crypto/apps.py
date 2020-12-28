from django.apps import AppConfig


class CryptoConfig(AppConfig):
    name = 'crypto'

    def ready(self):
        import crypto.signals
