import guide.models as models
from modeltranslation.translator import register, TranslationOptions


@register(models.Organization)
class OrganizationTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en', 'fr')


@register(models.CommodityType)
class CommodityTypeTO(TranslationOptions):
    fields = ['commodity_type']
    required_languages = ('en', 'fr')


@register(models.Code)
class CodeTO(TranslationOptions):
    fields = ['code']
    required_languages = ('en', 'fr')


@register(models.LimitedTenderingReason)
class LimitedTenderingReasonTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en', 'fr')


@register(models.GeneralException)
class GeneralExceptionTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en', 'fr')


@register(models.CftaException)
class CftaExceptionTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en', 'fr')