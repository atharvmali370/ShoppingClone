from django.apps import AppConfig


class UserappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userapp'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        import userapp.signals