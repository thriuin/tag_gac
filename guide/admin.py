from django.contrib import admin
from .models import GoodsCode, ConstructionCode, ServicesCode, TenderingReason, TAException, ValueThreshold, LimitedTendering
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


class LimitedTenderingResource(resources.ModelResource):

    class Meta:
        model = LimitedTendering


class LimitedTenderingAdmin(ImportExportModelAdmin):
    resource_class = LimitedTenderingResource


# Register your models here.
admin.site.register(GoodsCode, GoodsCodeAdmin)
admin.site.register(ConstructionCode, ConstructionCodeAdmin)
admin.site.register(ServicesCode, ServicesCodeAdmin)
admin.site.register(TAException, TAExceptionAdmin)
admin.site.register(TenderingReason, TenderingReasonAdmin)
admin.site.register(ValueThreshold, ValueThresholdAdmin)
admin.site.register(LimitedTendering, LimitedTenderingAdmin)


