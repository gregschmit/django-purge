from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelChoiceField
from . import models


class CustomContentTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{0} :: {1}".format(obj.app_label, obj)


class SettingsAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('name',) + list_filter + ('hour', 'day')
    search_fields = list_display
    fieldsets = (
            (None, { 'fields': ('name', 'active')}),
            ('Schedule', { 'fields': ('hour', 'day')}),
            )

    def get_queryset(self, request):
        models.Settings.get_active()
        query = super().get_queryset(request)
        return query


class DatabasePurgerAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('__str__',) + list_filter + ('delete_by_age', 'delete_by_quantity', 'datetime_field', 'age_in_days', 'max_records')
    search_fields = list_display
    fieldsets = (
            (None, { 'fields': ('table', 'active')}),
            ('Criteria', { 'fields': ('delete_by_age', 'delete_by_quantity', 'datetime_field', 'age_in_days', 'max_records')}),
            )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "table":
            return CustomContentTypeChoiceField(ContentType.objects.all(), **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(models.Settings, SettingsAdmin)
admin.site.register(models.DatabasePurger, DatabasePurgerAdmin)
