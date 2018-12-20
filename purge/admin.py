from django.contrib import admin
from . import models


class DatabasePurgerAdmin(admin.ModelAdmin):
    list_filter = ('enabled',)
    list_display = ('name',) + list_filter + ('selected_tables', 'delete_by_age', 'delete_by_quantity', 'datetime_field', 'age_in_days', 'max_records', 'day', 'time')
    search_fields = list_display
    fieldsets = (
            (None, { 'fields': ('name', 'enabled', 'tables')}),
            ('Schedule', { 'fields': ('day', 'time')}),
            ('Criteria', { 'fields': ('delete_by_age', 'delete_by_quantity', 'datetime_field', 'age_in_days', 'max_records')}),
            )
    filter_horizontal = ('tables',)


admin.site.register(models.DatabasePurger, DatabasePurgerAdmin)
