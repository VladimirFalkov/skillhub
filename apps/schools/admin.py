from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from core.admin import activate, deactivate
from schools.models import School, SchoolAlias, Advantages, Disadvantages


class CategoryResource(resources.ModelResource):

    class Meta:
        model = School


@admin.register(School)
class SchoolAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    actions = [activate, deactivate]


@admin.register(SchoolAlias)
class SchoolAliasAdmin(admin.ModelAdmin):
    pass

@admin.register(Advantages)
class AdvantagesAdmin(admin.ModelAdmin):
    pass

@admin.register(Disadvantages)
class DisadvantagesAdmin(admin.ModelAdmin):
    pass