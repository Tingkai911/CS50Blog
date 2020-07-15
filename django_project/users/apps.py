from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # import signals.py
    def ready(self):
        import users.signals