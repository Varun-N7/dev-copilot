from django.apps import AppConfig


class CopilotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'copilot'

    def ready(self):
        from copilot.db import embeddings_col
        print("MongoDB client initialised")