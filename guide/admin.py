from django.contrib import admin
from .models import GoodsCode, ConstructionCode, ServicesCode, TenderingReason, TAException, ValueThreshold
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Django Import-Export Registration (see: https://django-import-export.readthedocs.io)
class GoodsCodeResource(resources.ModelResource):

    class Meta:
        model = GoodsCode


class GoodsCodeAdmin(ImportExportModelAdmin):
    resource_class = GoodsCodeResource


class ConstructionCodeResource(resources.ModelResource):

    class Meta:
        model = ConstructionCode


class ConstructionCodeAdmin(ImportExportModelAdmin):
    resource_class = ConstructionCodeResource


class ServicesCodeResource(resources.ModelResource):

    class Meta:
        model = ServicesCode


class ServicesCodeAdmin(ImportExportModelAdmin):
    resource_class = ServicesCodeResource


# Register your models here.
admin.site.register(GoodsCode, GoodsCodeAdmin)
admin.site.register(ConstructionCode, ConstructionCodeAdmin)
admin.site.register(ServicesCode)
admin.site.register(TAException)
admin.site.register(TenderingReason)
admin.site.register(ValueThreshold)


