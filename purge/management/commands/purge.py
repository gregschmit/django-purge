from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from purge import models

class Command(BaseCommand):
    help = "Run all database purgers"

    def handle(self, *args, **options):
        """Run all database purgers"""
        models.DatabasePurger.purge_all()
