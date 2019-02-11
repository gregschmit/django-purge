from django.core.management import call_command
from django_cron import CronJobBase, Schedule
from .models import DatabasePurger


class CronJob(CronJobBase):
    schedule = Schedule(run_every_mins=240)
    code = 'django_purge.cron'

    def do(self):
        call_command('purge')
