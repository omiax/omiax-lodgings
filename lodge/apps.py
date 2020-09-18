from django.apps import AppConfig


class LodgeConfig(AppConfig):
    name = 'lodge'

    def ready(self):
        import lodge.signals  # noqa
