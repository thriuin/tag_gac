from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from api.models import Entities, ValueThreshold, \
    CommodityType, CommodityCodeSystem, CodeList, TenderingReason, \
    TAException, CftaException

# Django Import-Export Registration (see: https://django-import-export.readthedocs.io)


class EntitiesResource(resources.ModelResource):
    '''
    Admin resource for :model: 'api.Entities'
    '''
    class Meta:
        model=Entities


class ValueThresholdResource(resources.ModelResource):
    '''
    Admin resource for :model: 'api.ValueThreshold'
    '''
    class Meta:
        model=ValueThreshold


class CommodityTypeResource(resources.ModelResource):
    class Meta:
        model=CommodityType

class CommodityCodeSystemResource(resources.ModelResource):
    '''
    Admin resource for :model: 'api.CommodityCodeSystem
    '''
    class Meta:
        model=CommodityCodeSystem


class CodeListResource(resources.ModelResource):
    '''
    Admin resource for :model: 'api.CodeList'
    '''
    class Meta:
        model = CodeList


class TenderingReasonResource(resources.ModelResource):
    '''
    Admin resource for :model: 'api.TenderingReason'
    '''
    class Meta:
        model=TenderingReason


class TAExceptionResource(resources.ModelResource):
    '''
    Admin resource for :model: 'api.TAException'
    '''
    class Meta:
        model=TAException


class CftaExceptionResource(resources.ModelResource):
    '''
    Admin resource for :model: 'api.CftaException'
    '''
    class Meta:
        model=CftaException


class EntitiesAdmin(ImportExportModelAdmin):
    '''
    Admin import-export for :model: 'api.Entities'
    '''
    resource_class = EntitiesResource


class ValueThresholdAdmin(ImportExportModelAdmin):
    '''
    Admin import-export for :model: 'api.ValueThreshold'
    '''
    resource_class = ValueThresholdResource


class CommodityTypeAdmin(ImportExportModelAdmin):
    resource_class=CommodityTypeResource

class CommodityCodeSystemAdmin(ImportExportModelAdmin):
    '''
    Admin import-export for :model: api.CommodityCodeSystem
    '''
    resource_class = CommodityCodeSystemResource


class CodeListAdmin(ImportExportModelAdmin):
    '''
    Admin import-export for :model: 'api.CodeList'
    '''
    resource_class = CodeListResource


class TenderingReasonAdmin(ImportExportModelAdmin):
    '''
    Admin import-export for :model: 'api.TenderingReason'
    '''
    resource_class = TenderingReasonResource


class TAExceptionAdmin(ImportExportModelAdmin):
    '''
    Admin import-export for :model: 'api.TAException'
    '''
    resource_class = TAExceptionResource


class CftaExceptionAdmin(ImportExportModelAdmin):
    '''
    Admin import-export for :model: 'api.CftrException'
    '''
    resource_class = CftaExceptionResource




admin.site.register(Entities, EntitiesAdmin)
admin.site.register(ValueThreshold, ValueThresholdAdmin)
admin.site.register(CommodityType, CommodityTypeAdmin)
admin.site.register(CommodityCodeSystem, CommodityCodeSystemAdmin)
admin.site.register(CodeList, CodeListAdmin)
admin.site.register(TenderingReason, TenderingReasonAdmin)
admin.site.register(TAException, TAExceptionAdmin)
admin.site.register(CftaException, CftaExceptionAdmin)
