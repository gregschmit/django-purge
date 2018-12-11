from datetime import datetime, timedelta
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.utils import timezone


class Settings(models.Model):
    """
    This model represents the purger settings. It is important to ensure that
    all fields have sensible defaults.
    """
    name = models.CharField(max_length=255, blank=False)
    active = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)
    hour_choices = [(x, str(x)) for x in range(24)]
    hour = models.IntegerField(default=0, choices=hour_choices)
    day_choices = [(i-1, str(x)) for i, x in enumerate(['*', 'Su', 'M', 'Tu', 'W', 'Th', 'F', 'Sa'])]
    day = models.IntegerField(default=-1, choices=day_choices)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = verbose_name

    @classmethod
    def dcron_class_pattern(cls):
        s = cls.get_active()
        if not s.enabled: return ''
        if s.day == -1:
            d = '*'
        else:
            d = self.day
        return '0 {0} * * {1}'.format(s.hour, d)

    @classmethod
    def dcron_class_run(cls):
        call_command('purge')

    def save(self, *args, **kwargs):
        ss = type(self).objects.filter(active=True)
        if self.active:
            # deactivate all others
            for s in ss:
                if not s == self:
                    s.active = False
                    s.save()
        else:
            # ensure one other one is active, otherwise, activate this one
            if not ss:
                self.active = True
        return super().save(*args, **kwargs)

    @classmethod
    def get_active(cls):
        ss = cls.objects.filter(active=True)
        if ss:
            return ss[0]
        s = cls()
        s.name = "Default"
        s.save()
        return s


class DatabasePurger(models.Model):
    """
    This model represents another table in the database and a criteria for purging.
    """
    active = models.BooleanField(default=True)
    table = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    delete_by_age = models.BooleanField(default=True, help_text="Delete if entry is older than specified age")
    delete_by_quantity = models.BooleanField(default=False, help_text="Delete all except the youngest `max_records` entries")
    datetime_field = models.CharField(max_length=255, default='created')
    age_in_days = models.PositiveIntegerField(default=30)
    max_records = models.PositiveIntegerField(default=1000, help_text="Number of records to keep if `delete_by_quantity` is selected")

    class Meta:
        verbose_name = 'Database Purger'

    def __str__(self):
        return "{0} :: {1}".format(self.table.app_label, self.table)

    def purge(self):
        if not self.active: return
        m = self.table.model_class()
        d = timezone.now() - timedelta(days=self.age_in_days)
        datetime_filter = {self.datetime_field + '__lt': d}
        if self.delete_by_age:
            m.objects.filter(**datetime_filter).delete()
        if self.delete_by_quantity:
            x = m.objects.order_by('-' + self.datetime_field)[self.max_records:]
            m.objects.filter(pk__in=x).delete()

    @classmethod
    def purge_all(cls):
        for x in cls.objects.filter(active=True):
            x.purge()
