from django.contrib import admin
from guide.models import CommodityType, Code, GeneralException, TenderingReason, CftaException, ValueThreshold, Organization
from import_export import resources
from import_export.admin import ImportExportModelAdmin


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
        model = TenderingReason


class CftaExceptionResource(resources.ModelResource):

    class Meta:
        model = CftaException


class ValueThresholdResource(resources.ModelResource):

    class Meta:
        model = ValueThreshold


class OrganizationResource(resources.ModelResource):

    class Meta:
        model = Organization


class CommodityTypeAdmin(ImportExportModelAdmin):
    resource_class = CommodityTypeResource


class CodeAdmin(ImportExportModelAdmin):
    resource_class = CodeResource


class GeneralExceptionAdmin(ImportExportModelAdmin):
    resource_class = GeneralExceptionResource


class TenderingReasonAdmin(ImportExportModelAdmin):
    resource_class = TenderingReasonResource


class CftaExceptionAdmin(ImportExportModelAdmin):
    resource_class = CftaExceptionResource


class ValueThresholdAdmin(ImportExportModelAdmin):
    resource_class = ValueThresholdResource


class OrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationResource


# Register your models here
admin.site.register(CommodityType, CommodityTypeAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(GeneralException, GeneralExceptionAdmin)
admin.site.register(TenderingReason, TenderingReasonAdmin)
admin.site.register(CftaException, CftaExceptionAdmin),
admin.site.register(ValueThreshold, ValueThresholdAdmin)
admin.site.register(Organization, OrganizationAdmin)
