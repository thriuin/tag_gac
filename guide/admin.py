from django.contrib import admin
from guide.models import CommodityType, Code, GeneralException, LimitedTenderingReason, CftaException, ValueThreshold, Organization, OrganizationWithCommodityCodeRules, OrganizationWithCommodityTypeRules
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Model resources
class OrganizationWithCommodityTypeRulesResource(resources.ModelResource):

    class Meta:
        model = OrganizationWithCommodityTypeRules


class OrganizationWithCommodityCodeRulesResource(resources.ModelResource):

    class Meta:
        model = OrganizationWithCommodityCodeRules


class CommodityTypeResource(resources.ModelResource):

    class Meta:
        model = CommodityType


class CodeResource(resources.ModelResource):

    class Meta:
        model = Code


class GeneralExceptionResource(resources.ModelResource):

    class Meta:
        model = GeneralException


class TenderingReasonResource(resources.ModelResource):

    class Meta:
        model = LimitedTenderingReason


class CftaExceptionResource(resources.ModelResource):

    class Meta:
        model = CftaException


class ValueThresholdResource(resources.ModelResource):

    class Meta:
        model = ValueThreshold


class OrganizationResource(resources.ModelResource):

    class Meta:
        model = Organization


# ImportExportModelAdmins
class OrganizationWithCommodityCodeRulesAdmin(ImportExportModelAdmin):
    resource_class = OrganizationWithCommodityTypeRulesResource
    list_display = [f.name for f in CommodityType._meta.get_fields()][::-1]
    list_editable = [f.name for f in CommodityType._meta.get_fields() if f.name != 'id']
    list_display_links = ['id']
    

class OrganizationWithCommodityTypeRulesAdmin(ImportExportModelAdmin):
    resource_class = OrganizationWithCommodityTypeRulesResource
    list_display = [f.name for f in CommodityType._meta.get_fields()][::-1]
    list_editable = [f.name for f in CommodityType._meta.get_fields() if f.name != 'id']
    list_display_links = ['id']


class CommodityTypeAdmin(ImportExportModelAdmin):
    resource_class = CommodityTypeResource
    list_display = [f.name for f in CommodityType._meta.get_fields()][::-1]
    list_editable = [f.name for f in CommodityType._meta.get_fields() if f.name != 'id']
    list_display_links = ['id']


class CodeAdmin(ImportExportModelAdmin):
    resource_class = CodeResource
    list_display = [f.name for f in Code._meta.get_fields()][::-1]
    list_editable = [f.name for f in Code._meta.get_fields() if f.name != 'id']
    list_display_links = ['id']


class GeneralExceptionAdmin(ImportExportModelAdmin):
    resource_class = GeneralExceptionResource
    list_display = [f.name for f in GeneralException._meta.get_fields()][::-1]
    list_editable = [f.name for f in GeneralException._meta.get_fields() if f.name != 'id']
    list_display_links = ['id']


class TenderingReasonAdmin(ImportExportModelAdmin):
    resource_class = TenderingReasonResource
    list_display = [f.name for f in LimitedTenderingReason._meta.get_fields()][::-1]
    list_editable = [f.name for f in LimitedTenderingReason._meta.get_fields() if f.name != 'id']
    list_display_links = ['id']


class CftaExceptionAdmin(ImportExportModelAdmin):
    resource_class = CftaExceptionResource
    list_display = [f.name for f in CftaException._meta.get_fields()][::-1]
    list_editable = [f.name for f in CftaException._meta.get_fields() if f.name != 'id']
    list_display_links = ['id']


class ValueThresholdAdmin(ImportExportModelAdmin):
    resource_class = ValueThresholdResource
    list_display = [f.name for f in ValueThreshold._meta.get_fields()][::-1]
    list_editable = [f.name for f in ValueThreshold._meta.get_fields() if (f.name != 'id' and f.name != 'type_value')]
    list_display_links = ['id']


class OrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationResource
    list_display = [f.name for f in Organization._meta.get_fields()][::-1]
    list_editable = [f.name for f in Organization._meta.get_fields() if f.name != 'id']
    list_display_links = ['id']

# Register your models here
admin.site.register(CommodityType, CommodityTypeAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(GeneralException, GeneralExceptionAdmin)
admin.site.register(LimitedTenderingReason, TenderingReasonAdmin)
admin.site.register(CftaException, CftaExceptionAdmin),
admin.site.register(ValueThreshold, ValueThresholdAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationWithCommodityTypeRules, OrganizationWithCommodityTypeRulesAdmin)
admin.site.register(OrganizationWithCommodityCodeRules, OrganizationWithCommodityCodeRulesAdmin)