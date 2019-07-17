from datetime import datetime, timedelta
from dateutil import parser
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from fnmatch import fnmatchcase
import os
import stat
import sys


class DatabasePurger(models.Model):
    """Represents a purging action on a set of database tables."""
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    tables = models.ManyToManyField(ContentType)
    delete_by_age = models.BooleanField(default=True, help_text="Delete if entry is older than specified age")
    delete_by_quantity = models.BooleanField(default=False, help_text="Delete all except the youngest `max_records` entries")
    datetime_field = models.CharField(max_length=255, default='created', help_text="Date or datetime field used to determine the age of a record")
    age_in_days = models.PositiveIntegerField(default=30, help_text="If `delete_by_age` is selected, delete records older than this age")
    max_records = models.PositiveIntegerField(default=1000, help_text="Number of records to keep if `delete_by_quantity` is selected")

    @property
    def selected_tables(self):
        """Getter to display the selected tables in the admin UI."""
        return '<br>'.join([str(x) for x in self.tables.all()])

    def __str__(self):
        return self.name

    def purge(self):
        """
        If this purger is enabled, purge the selected tables by age/quantity
        depending on the configuration.
        """
        if not self.enabled: return
        model_list = [x.model_class() for x in self.tables.all()]
        d = timezone.now() - timedelta(days=self.age_in_days)
        datetime_filter = {self.datetime_field + '__lt': d}
        date_filter = {self.datetime_field + '__lt': d.date()}
        if self.delete_by_age:
            for m in model_list:
                try:
                    m.objects.filter(**datetime_filter).delete()
                except TypeError: # field is datefield, not datetimefield
                    m.objects.filter(**date_filter).delete()
        if self.delete_by_quantity:
            for m in model_list:
                x = m.objects.order_by('-' + self.datetime_field)[self.max_records:]
                m.objects.filter(pk__in=x).delete()

    @classmethod
    def purge_all(cls):
        """Helper for running purge on all of the `DatabasePurger`'s."""
        for x in cls.objects.filter(enabled=True):
            x.purge()


class FilePurger(models.Model):
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    file_pattern = models.CharField(max_length=255, help_text="Pattern of files to inspect using POSIX shell expansion (e.g., 'datafile-.*\.txt')")
    directory = models.CharField(max_length=255, blank=True)
    recursive_search = models.BooleanField(default=False, help_text="Search directories recursively")
    delete_by_filename = models.BooleanField(default=True, blank=True, help_text="Delete by timestamp in filename")
    filename_date_year_first = models.BooleanField(default=False, help_text="Whether we should expect the year to come first")
    filename_date_day_first = models.BooleanField(default=False, help_text="Whether we should expect the day to come before the month")
    delete_by_atime = models.BooleanField(default=False, help_text="Delete if access time is too old")
    delete_by_mtime = models.BooleanField(default=True, help_text="Delete if modification time is too old")
    delete_by_ctime = models.BooleanField(default=False, help_text="Delete if (meta) change time is too old")
    age_in_days = models.PositiveIntegerField(default=30, help_text="Delete records older than this age")

    def __str__(self):
        return self.name

    def filename_is_older_than(self, filename, dt):
        """
        Extract the datetime object from a filename and check it to see if it
        is too old.
        """
        try:
            file_date = parser.parse(filename, fuzzy=True, dayfirst=self.filename_date_day_first, yearfirst=self.filename_date_year_first)
        except ValueError:
            return False
        return file_date < dt

    def purge_recursive(self, dt, directory=None):
        """
        Purge files in this directory that match the criteria, and be recursive
        if that option is selected.
        """
        if not directory: directory = self.directory
        subdirs = []
        try:
            listing = os.listdir(directory)
        except FileNotFoundError:
            listing = []
        for f in listing:
            fqf = os.path.join(directory, f)
            s = os.stat(fqf, follow_symlinks=False)
            if stat.S_ISDIR(s.st_mode):
                subdirs.append(fqf)
                continue
            if not fnmatchcase(f, self.file_pattern):
                continue
            if self.delete_by_filename and self.filename_is_older_than(f, dt):
                print("purge: removing {} because of filename".format(fqf), file=sys.stderr)
                os.remove(fqf)
            elif self.delete_by_atime and (datetime.fromtimestamp(s.st_atime) < dt):
                print("purge: removing {} because of atime".format(fqf), file=sys.stderr)
                os.remove(fqf)
            elif self.delete_by_mtime and (datetime.fromtimestamp(s.st_mtime) < dt):
                print("purge: removing {} because of mtime".format(fqf), file=sys.stderr)
                os.remove(fqf)
            elif self.delete_by_ctime and (datetime.fromtimestamp(s.st_ctime) < dt):
                print("purge: removing {} because of ctime".format(fqf), file=sys.stderr)
                os.remove(fqf)
        if self.recursive_search:
            for sd in subdirs:
                self.purge_recursive(dt, os.path.join(directory, sd))


    def purge(self, directory=None):
        """
        If this purger is enabled, evaluate the date and call the recursive
        purge method.
        """
        if not self.enabled: return
        d = timezone.now() - timedelta(days=self.age_in_days)
        self.purge_recursive(d.replace(tzinfo=None))

    @classmethod
    def purge_all(cls):
        """Helper for running purge on all of the `FilePurger`'s."""
        for x in cls.objects.filter(enabled=True):
            x.purge()
