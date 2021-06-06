from django.apps import AppConfig


class EndpointsConfig(AppConfig):
    name = 'endpoints'
    
    """
    ready(): is responsible for triggering @receiver decorator
    in signals
    """
    
    def ready(self):
        import endpoints.signals
