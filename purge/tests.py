"""
Unit tests
"""
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from .models import DatabasePurger, FilePurger


class DatabasePurgerTestCase(TestCase):
    """
    Tests for the ``DatabasePurger`` model.
    """
    def setUp(self):
        self.d = DatabasePurger(
            name='test1',
            datetime_field='action_time',
            delete_by_quantity=True,
        )
        self.d.save()
        self.d.tables.add(ContentType.objects.get(
            app_label='admin',
            model='logentry',
        ))

    def test_selected_tables(self):
        """
        Test the ``selected_tables`` method.
        """
        self.assertEqual(self.d.selected_tables, str(self.d.tables.all()[0]))

    def test_purge(self):
        """
        Test the ``purge`` method on an instance.
        """
        self.assertIsNone(self.d.purge())

    def test_purge_all(self):
        """
        Test the main ``purge_all`` class method.
        """
        self.assertIsNone(DatabasePurger.purge_all())


class FilePurgerTestCase(TestCase):
    """
    Tests for the ``FilePurger`` model.

    WARNING: Be careful not to actually interact with the file system!
    """
    def setUp(self):
        self.f = FilePurger(
            name='test2',
            file_pattern='TEST',
            delete_by_filename=False,
            delete_by_atime=False,
            delete_by_mtime=False,
            delete_by_ctime=False,
        )
        self.f.save()

    def test_purge(self):
        """
        Test the ``purge`` method on an instance.
        """
        self.assertIsNone(self.f.purge())

    def test_purge_all(self):
        """
        Test the main ``purge_all`` class method.
        """
        self.assertIsNone(FilePurger.purge_all())
