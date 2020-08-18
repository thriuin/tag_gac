from django.contrib import admin
import guide.models as models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin
from guide.logic import AGREEMENTS

# Model resources
class OrgTypeRuleResource(resources.ModelResource):

    class Meta:
        model = models.OrgTypeRule



class CodeOrganizationExclusionResource(resources.ModelResource):

    class Meta:
        model = models.CodeOrganizationExclusion


class CommodityTypeResource(resources.ModelResource):

    class Meta:
        model = models.CommodityType


class CodeResource(resources.ModelResource):

    class Meta:
        model = models.Code


class GeneralExceptionResource(resources.ModelResource):

    class Meta:
        model = models.GeneralException


class TenderingReasonResource(resources.ModelResource):

    class Meta:
        model = models.LimitedTenderingReason


class CftaExceptionResource(resources.ModelResource):

    class Meta:
        model = models.CftaException


class ValueThresholdResource(resources.ModelResource):

    class Meta:
        model = models.ValueThreshold


class OrganizationResource(resources.ModelResource):

    class Meta:
        model = models.Organization


class ListDisplayMixin(object):
    def __init__(self, model, admin_site):
        lst = [f.name for f in model._meta.get_fields()]
        self.list_display = list(reversed(lst))
        self.list_editable = list(filter(lambda x: x != 'id', lst))
        self.list_display_links = ['id']
        super(ListDisplayMixin, self).__init__(model, admin_site)


# ModelAdmins
@admin.register(models.OrgTypeRule)
class TypeOrganizationExclusionAdmin(ListDisplayMixin, ImportExportModelAdmin):
    resource_class = OrgTypeRuleResource
    list_filter = AGREEMENTS
    search_fields = ['org_fk']


@admin.register(models.CodeOrganizationExclusion)
class CodeOrganizationExclusionAdmin(ListDisplayMixin, ImportExportModelAdmin):
    resource_class = CodeOrganizationExclusionResource
    list_filter = AGREEMENTS
    search_fields = ['org_fk', 'code_fk']


@admin.register(models.CommodityType)
class CommodityTypeAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = CommodityTypeResource


@admin.register(models.Code)
class CodeAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = CodeResource
    lst = AGREEMENTS.copy()
    lst.append('type')
    list_filter = lst
    search_fields = ['code', 'code_en', 'code_fr']


@admin.register(models.GeneralException)
class GeneralExceptionAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = GeneralExceptionResource
    list_filter = AGREEMENTS
    search_fields = ['description', 'description_en', 'description_fr']


@admin.register(models.LimitedTenderingReason)
class TenderingReasonAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = TenderingReasonResource
    list_filter = AGREEMENTS
    search_fields = ['description', 'description_en', 'description_fr']


@admin.register(models.CftaException)
class CftaExceptionAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = CftaExceptionResource
    search_fields = ['description', 'description_en', 'description_fr']


@admin.register(models.ValueThreshold)
class ValueThresholdAdmin(ListDisplayMixin, ImportExportModelAdmin):
    resource_class = ValueThresholdResource
    list_filter = ['type']


@admin.register(models.Organization)
class OrganizationAdmin(ListDisplayMixin, ImportExportModelAdmin, TranslationAdmin):
    resource_class = OrganizationResource
    list_filter = AGREEMENTS
    search_fields = ['entities', 'entities_en', 'entities_fr']
