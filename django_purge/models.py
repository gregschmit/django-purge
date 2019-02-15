import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class DatabasePurger(models.Model):
    """Represents a purging action on a set of database tables."""
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    tables = models.ManyToManyField(ContentType)
    delete_by_age = models.BooleanField(default=True, help_text="Delete if entry is older than specified age")
    delete_by_quantity = models.BooleanField(default=False, help_text="Delete all except the youngest `max_records` entries")
    datetime_field = models.CharField(max_length=255, default='created', help_text="Field used to determine the age of a record")
    age_in_days = models.PositiveIntegerField(default=30, help_text="If `delete_by_age` is selected, delete records older than this age")
    max_records = models.PositiveIntegerField(default=1000, help_text="Number of records to keep if `delete_by_quantity` is selected")

    class Meta:
        verbose_name = 'Database Purger'

    @property
    def selected_tables(self):
        """Getter to display the selected tables in the admin UI."""
        return '\n'.join([str(x) for x in self.tables.all()])

    def dcron_run(self):
        """run == purge for a model instance"""
        self.purge()

    def __str__(self):
        return self.name

    def purge(self):
        """
        If this purger is enabled, purge the selected tables by age/quantity
        depending on the configuration.
        """
        if not self.enabled: return
        model_list = [x.model_class() for x in self.tables.all()]
        d = timezone.now() - datetime.timedelta(days=self.age_in_days)
        datetime_filter = {self.datetime_field + '__lt': d}
        if self.delete_by_age:
            for m in model_list:
                m.objects.filter(**datetime_filter).delete()
        if self.delete_by_quantity:
            for m in model_list:
                x = m.objects.order_by('-' + self.datetime_field)[self.max_records:]
                m.objects.filter(pk__in=x).delete()

    @classmethod
    def purge_all(cls):
        """Helper for running purge on all of the `DatabasePurger`'s."""
        for x in cls.objects.filter(enabled=True):
            x.purge()
