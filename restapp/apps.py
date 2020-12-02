from django.apps import AppConfig


class RestappConfig(AppConfig):
    name = 'restapp'

    def ready(self):
        print("Hiiiii")