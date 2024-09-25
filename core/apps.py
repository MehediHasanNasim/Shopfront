from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
<<<<<<< HEAD
    
    def ready(self) -> None:
        import core.signals.handlers 
=======
>>>>>>> c05b93e92ee79022cda30f15f3de326f4cfa90e7
