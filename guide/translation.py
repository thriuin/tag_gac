from guide.models import CommodityType, Code, GeneralException, LimitedTenderingReason, CftaException, ValueThreshold, Organization, OrganizationWithCommodityCodeRule, OrganizationWithCommodityTypeRule
from modeltranslation.translator import register, TranslationOptions


@register(Organization)
class OrganizationTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en-ca', 'fr-ca')


@register(CommodityType)
class CommodityTypeTO(TranslationOptions):
    fields = ['commodity_type']
    required_languages = ('en-ca', 'fr-ca')


@register(Code)
class CodeTO(TranslationOptions):
    fields = ['code']
    required_languages = ('en-ca', 'fr-ca')


@register(LimitedTenderingReason)
class LimitedTenderingReasonTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en-ca', 'fr-ca')


@register(GeneralException)
class GeneralExceptionTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en-ca', 'fr-ca')


@register(CftaException)
class CftaExceptionTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en-ca', 'fr-ca')