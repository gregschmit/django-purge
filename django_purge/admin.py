from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelMultipleChoiceField
from django.utils.html import format_html
from . import models


class CustomModelMCF(ModelMultipleChoiceField):
    widget = FilteredSelectMultiple("Models", False)

    def label_from_instance(self, obj):
        return "{0} :: {1}".format(obj.app_label, obj)


class DatabasePurgerAdmin(admin.ModelAdmin):
    list_filter = ('enabled',)
    list_display = ('name',) + list_filter + ('_selected_tables', 'delete_by_age', 'delete_by_quantity', 'datetime_field', 'age_in_days', 'max_records')
    search_fields = list_display
    fieldsets = (
        (None, { 'fields': ('name', 'enabled', 'tables')}),
        ('Criteria', { 'fields': ('delete_by_age', 'delete_by_quantity', 'datetime_field', 'age_in_days', 'max_records')}),
    )

    def _selected_tables(self, obj):
        return format_html(obj.selected_tables)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tables':
            return CustomModelMCF(ContentType.objects.all(), **kwargs)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class FilePurgerAdmin(admin.ModelAdmin):
    list_filter = ('enabled',)
    list_display = ('name',) + list_filter + ('file_pattern', 'directory', 'recursive_search', 'delete_by_filename', 'filename_date_year_first', 'filename_date_day_first', 'delete_by_atime', 'delete_by_mtime', 'delete_by_ctime', 'age_in_days')
    search_fields = list_display
    fieldsets = (
        (None, { 'fields': ('name', 'enabled', 'file_pattern', 'directory', 'recursive_search')}),
        ('Criteria', { 'fields': ('delete_by_filename', 'filename_date_year_first', 'filename_date_day_first', 'delete_by_atime', 'delete_by_mtime', 'delete_by_ctime', 'age_in_days')}),
    )


admin.site.register(models.DatabasePurger, DatabasePurgerAdmin)
admin.site.register(models.FilePurger, FilePurgerAdmin)
