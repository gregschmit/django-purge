from django.apps import AppConfig
from .version import get_version


class CustomConfig(AppConfig):
    name = 'purge'
    verbose_name = "Purge - v" + get_version()
