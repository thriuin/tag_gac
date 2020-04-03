from django.contrib import admin
from guide.models import CommodityType, CommodityCodeSystem, Code, TAException, TenderingReason, CftaException, ValueThreshold, Entities, Instructions
from import_export import resources
from import_export.admin import ImportExportModelAdmin



class CommodityTypeResource(resources.ModelResource):

    class Meta:
        model = CommodityType


class CommodityCodeSystemResource(resources.ModelResource):

    class Meta:
        model = CommodityCodeSystem

class CodeResource(resources.ModelResource):

    class Meta:
        model = Code


class TAExceptionResource(resources.ModelResource):

    class Meta:
        model = TAException


class TenderingReasonResource(resources.ModelResource):

    class Meta:
        model = TenderingReason


class CftaExceptionResource(resources.ModelResource):

    class Meta:
        model = CftaException

class ValueThresholdResource(resources.ModelResource):

    class Meta:
        model = ValueThreshold


class EntitiesResource(resources.ModelResource):

    class Meta:
        model = Entities


class InstructionsResource(resources.ModelResource):

    class Meta:
        model = Instructions


class CommodityTypeAdmin(ImportExportModelAdmin):
    resource_class = CommodityTypeResource

class CommodityCodeSystemAdmin(ImportExportModelAdmin):
    resource_class = CommodityCodeSystemResource

class CodeAdmin(ImportExportModelAdmin):
    resource_class = CodeResource

class TAExceptionAdmin(ImportExportModelAdmin):
    resource_class = TAExceptionResource

class TenderingReasonAdmin(ImportExportModelAdmin):
    resource_class = TenderingReasonResource

class CftaExceptionAdmin(ImportExportModelAdmin):
    resource_class = CftaExceptionResource

class ValueThresholdAdmin(ImportExportModelAdmin):
    resource_class = ValueThresholdResource

class EntitiesAdmin(ImportExportModelAdmin):
    resource_class = EntitiesResource

class InstructionsAdmin(ImportExportModelAdmin):
    resource_class = InstructionsResource

# Register your models here
admin.site.register(CommodityType, CommodityTypeAdmin)
admin.site.register(CommodityCodeSystem, CommodityCodeSystemAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(TAException, TAExceptionAdmin)
admin.site.register(TenderingReason, TenderingReasonAdmin)
admin.site.register(CftaException, CftaExceptionAdmin),
admin.site.register(ValueThreshold, ValueThresholdAdmin)
admin.site.register(Entities, EntitiesAdmin)
admin.site.register(Instructions, InstructionsAdmin)