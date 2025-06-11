from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'Django-Chat.Models'

    def ready(self):
        import Django-Chat.Models.signals
o

