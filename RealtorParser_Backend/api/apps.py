from django.apps import AppConfig
from RealtorParser_Backend.config import config


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        if config.getboolean('APP', 'parser'):
            from api import updater
            updater.start()
