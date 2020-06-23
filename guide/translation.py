# from guide.models import CommodityType, Code, GeneralException, LimitedTenderingReason, CftaException, ValueThreshold, Organization, OrganizationWithCommodityCodeRules, OrganizationWithCommodityTypeRules
# from modeltranslation.translator import register, TranslationOptions


# @register(Organization)
# class OrganizationTO(TranslationOptions):
#     fields = ['name']
#     required_languages = ('en-ca', 'fr-ca')

# @register(CommodityType)
# class CommodityTypeTO(TranslationOptions):
#     fields = ['commodity_type']


# @register(Code)
# class CodeTO(TranslationOptions):
#     fields = ['code']


# @register(LimitedTenderingReason)
# class LimitedTenderingReasonTO(TranslationOptions):
#     fields = ['name']


# @register(GeneralException)
# class GeneralExceptionTO(TranslationOptions):
#     fields = ['name']


# @register(CftaException)
# class CftaExceptionTO(TranslationOptions):
#     fields = ['name']