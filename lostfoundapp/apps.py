from django.apps import AppConfig


class LostfoundappConfig(AppConfig):
    name = 'lostfoundapp'
    def ready(self):
        import lostfoundapp.signals
