from django.contrib import admin
from guide.models import CommodityType, Code, GeneralException, LimitedTenderingReason, CftaException, ValueThreshold, Organization, OrganizationWithCommodityCodeRule, OrganizationWithCommodityTypeRule
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin
from guide.logic import AGREEMENTS

# Model resources
class OrganizationWithCommodityTypeRuleResource(resources.ModelResource):

    class Meta:
        model = OrganizationWithCommodityTypeRule


class OrganizationWithCommodityCodeRuleResource(resources.ModelResource):

    class Meta:
        model = OrganizationWithCommodityCodeRule


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


class ListDisplayMixin(object):
    def __init__(self, model, admin_site):
        lst = [f.name for f in model._meta.get_fields()]
        self.list_display = list(reversed(lst))
        self.list_editable = list(filter(lambda x: x != 'id', lst))
        self.list_display_links = ['id']
        super(ListDisplayMixin, self).__init__(model, admin_site)


# ModelAdmins
@admin.register(OrganizationWithCommodityCodeRule)
class OrganizationWithCommodityCodeRulesAdmin(ListDisplayMixin, ImportExportModelAdmin):
    resource_class = OrganizationWithCommodityCodeRuleResource
    list_filter = AGREEMENTS
    search_fields = ['org_fk']


@admin.register(OrganizationWithCommodityTypeRule)
class OrganizationWithCommodityTypeRuleAdmin(ListDisplayMixin, ImportExportModelAdmin):
    resource_class = OrganizationWithCommodityTypeRuleResource
    list_filter = AGREEMENTS
    search_fields = ['org_fk', 'code_fk']


@admin.register(CommodityType)
class CommodityTypeAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = CommodityTypeResource


@admin.register(Code)
class CodeAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = CodeResource
    lst = AGREEMENTS.copy()
    lst.append('type')
    list_filter = lst
    search_fields = ['code', 'code_en', 'code_fr']


@admin.register(GeneralException)
class GeneralExceptionAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = GeneralExceptionResource
    list_filter = AGREEMENTS
    search_fields = ['description', 'description_en', 'description_fr']


@admin.register(LimitedTenderingReason)
class TenderingReasonAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = TenderingReasonResource
    list_filter = AGREEMENTS
    search_fields = ['description', 'description_en', 'description_fr']


@admin.register(CftaException)
class CftaExceptionAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = CftaExceptionResource
    search_fields = ['description', 'description_en', 'description_fr']


@admin.register(ValueThreshold)
class ValueThresholdAdmin(ListDisplayMixin, ImportExportModelAdmin):
    resource_class = ValueThresholdResource
    list_filter = ['type']


@admin.register(Organization)
class OrganizationAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = OrganizationResource
    list_filter = AGREEMENTS
    search_fields = ['entities', 'entities_en', 'entities_fr']
