from django.contrib import admin
from .models import CommodityTypes, CommodityCodingSystem, CommodityCode, TenderingReason, TAException, ValueThreshold, CftaExceptions, Entities
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Django Import-Export Registration (see: https://django-import-export.readthedocs.io)

class CommodityTypesResource(resources.ModelResource):

    class Meta:
        model = CommodityTypes


class CommodityTypesAdmin(ImportExportModelAdmin):
    resource_class = CommodityTypesResource


class CommodityCodingSystemRessource(resources.ModelResource):

    class Meta:
        model = CommodityCodingSystem


class CommodityCodingSystemAdmin(ImportExportModelAdmin):
    resource_class = CommodityCodingSystemRessource


class CommodityCodeResource(resources.ModelResource):
    
    class Meta:
        model = CommodityCode


class CommodityCodeAdmin(ImportExportModelAdmin):
    resource_class = CommodityCodeResource


class TenderingReasonResource(resources.ModelResource):

    class Meta:
        model = TenderingReason


class TenderingReasonAdmin(ImportExportModelAdmin):
    resource_class = TenderingReasonResource


class TAExceptionResource(resources.ModelResource):

    class Meta:
        model = TAException


class TAExceptionAdmin(ImportExportModelAdmin):
    resource_class = TAExceptionResource


class ValueThresholdResource(resources.ModelResource):

    class Meta:
        model = ValueThreshold


class ValueThresholdAdmin(ImportExportModelAdmin):
    resource_class = ValueThresholdResource


class CftaExceptionResource(resources.ModelResource):

    class Meta:
        model = CftaExceptions


class CftaExceptionAdmin(ImportExportModelAdmin):
    resource_class = CftaExceptionResource


class EntitiesResource(resources.ModelResource):

    class Meta:
        model = Entities


class EntitiesAdmin(ImportExportModelAdmin):
    resource_class = EntitiesResource


# Register your models here.
admin.site.register(CommodityTypes, CommodityTypesAdmin)
admin.site.register(CommodityCodingSystem, CommodityCodingSystemAdmin)
admin.site.register(CommodityCode, CommodityCodeAdmin)
admin.site.register(TAException, TAExceptionAdmin)
admin.site.register(TenderingReason, TenderingReasonAdmin)
admin.site.register(ValueThreshold, ValueThresholdAdmin)
admin.site.register(CftaExceptions, CftaExceptionAdmin)
admin.site.register(Entities, EntitiesAdmin)

