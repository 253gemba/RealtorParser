from django.apps import AppConfig
from RealtorParser_Backend.config import config


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        if config.getboolean('APP', 'parser'):
            from base import updater
            updater.start()