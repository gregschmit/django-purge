from django.contrib import admin
from . import models


class SettingAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('name',) + list_filter + ('hour', 'day')
    search_fields = list_display
    fieldsets = (
            (None, { 'fields': ('name', 'active')}),
            ('Schedule', { 'fields': ('hour', 'day')}),
            )

    def get_queryset(self, request):
        models.Setting.get_active()
        query = super().get_queryset(request)
        return query


class DatabasePurgerAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('table',) + list_filter + ('delete_by_age', 'delete_by_quantity', 'datetime_field', 'age_in_days', 'n')
    search_fields = list_display
    fieldsets = (
            (None, { 'fields': ('table', 'active')}),
            ('Criteria', { 'fields': ('delete_by_age', 'delete_by_quantity', 'datetime_field', 'age_in_days', 'n')}),
            )


admin.site.register(models.Setting, SettingAdmin)
admin.site.register(models.DatabasePurger, DatabasePurgerAdmin)
