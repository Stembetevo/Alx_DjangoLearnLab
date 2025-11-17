from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'

    def ready(self):
        # Import signal handlers to ensure they are registered when the app is ready
        from . import signals  # noqa: F401
