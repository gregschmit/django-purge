from django.core.management import call_command
from django_cron import CronJobBase, Schedule
from .models import DatabasePurger
from .settings import get_setting


class CronJob(CronJobBase):
    schedule = Schedule(run_at_times=get_setting('PURGE_CRON_RUN_AT_TIMES'))
    code = 'purge.cron'

    def do(self):
        call_command('purge')
