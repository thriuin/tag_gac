from guide.models import CommodityType, Code, GeneralException, LimitedTenderingReason, CftaException, ValueThreshold, Organization, OrganizationWithCommodityCodeRules, OrganizationWithCommodityTypeRules

from modeltranslation.translator import register, TranslationOptions
CommodityType, Code, GeneralException, LimitedTenderingReason, CftaException, ValueThreshold, Organization, OrganizationWithCommodityCodeRules, OrganizationWithCommodityTypeRules


@register(Organization):
class OrganizationTO(TranslationOptions):
    fields = ('name')


@register(CommodityType):
class CommodityTypeTO(TranslationOptions):
    fields = ('commodity_type')


@register(Code):
class CodeTO(TranslationOptions):
    fields = ('type', 'code')


@register(OrganizationWithCommodityCodeRules)
class OrganizationWithCommodityCodeRulesTO(TranslationOptions):
    fields = ('com_type', 'tc', 'goods_rule')


@register(OrganizationWithCommodityTypeRules)
class OrganizationWithCommodityTypeRulesTO(TranslationOptions):
    fields = ('code_fk', 'org_fk')


@register(LimitedTenderingReason)
class LimitedTenderingReasonTO(TranslationOptions):
    fields = ('name')


@register(GeneralException)
class GeneralExceptionTO(TranslationOptions):
    fields = ('name')


@register(CftaException)
class CftaExceptionTO(TranslationOptions):
    fields = ('name')