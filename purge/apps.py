from django.apps import AppConfig
from .version import get_version


class CustomConfig(AppConfig):
    name = 'purge'
    verbose_name = "purge - v" + get_version()
