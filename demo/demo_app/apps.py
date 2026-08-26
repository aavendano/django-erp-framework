"""Demo App Config."""
from django.apps import AppConfig


class DemoAppConfig(AppConfig):
    name = 'demo_app'
    verbose_name = 'Demo App'
    
    def ready(self):
        super().ready()
        # Import reports to register them
        from . import reports  # noqa: F401
