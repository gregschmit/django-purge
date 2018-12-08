from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from purge import models

class Command(BaseCommand):
    help = 'This command purges the database of any entries that match the criteria.'

    def handle(self, *args, **options):
        models.DatabasePurger.purge_all()
