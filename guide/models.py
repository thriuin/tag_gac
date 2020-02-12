from django.db import models


class BooleanTradeAgreement(models.Model):

    id = models.AutoField(primary_key=True)
    nafta_annex = models.BooleanField(default=False, verbose_name="NAFTA Annex 1001.1b-1", blank=False)
    ccfta = models.BooleanField(default=False, verbose_name="Chile (CCFTA) Annex K bis-01.1-3", blank=False)
    ccofta = models.BooleanField(default=False, verbose_name="Colombia (CCoFTA) Annex 1401-4", blank=False)
    chfta = models.BooleanField(default=False, verbose_name="Honduras (CHFTA) Annex 17.3", blank=False)
    cpafta = models.BooleanField(default=False, verbose_name="Panama (CPaFTA) Annex 4", blank=False)
    cpfta = models.BooleanField(default=False, verbose_name="Peru (CPFTA) Annex 1401. 1-3", blank=False)
    ckfta = models.BooleanField(default=False, verbose_name="Korea (CKFTA) Annex 14-A", blank=False)
    cufta = models.BooleanField(default=False, verbose_name="Ukraine (CUFTA) Annex 10-3", blank=False)
    wto_agp = models.BooleanField(default=False, verbose_name="WTO-AGP Canada Annex 1", blank=False)
    ceta = models.BooleanField(default=False, verbose_name="CETA Annex 19-4", blank=False)
    cptpp = models.BooleanField(default=False, verbose_name="CPTPP Chapter 15-A Section D", blank=False)
    cfta = models.BooleanField(default=False, verbose_name="CFTA Chapter 5", blank=False)


class NumericTradeAgreements(models.Model):

    id = models.AutoField(primary_key=True)
    nafta_annex = models.IntegerField(default=0, verbose_name="NAFTA Annex 1001.1b-1", blank=False)
    ccfta = models.IntegerField(default=0, verbose_name="Chile (CCFTA) Annex K bis-01.1-3", blank=False)
    ccofta = models.IntegerField(default=0, verbose_name="Colombia (CCoFTA) Annex 1401-4", blank=False)
    chfta = models.IntegerField(default=0, verbose_name="Honduras (CHFTA) Annex 17.3", blank=False)
    cpafta = models.IntegerField(default=0, verbose_name="Panama (CPaFTA) Annex 4", blank=False)
    cpfta = models.IntegerField(default=0, verbose_name="Peru (CPFTA) Annex 1401. 1-3", blank=False)
    ckfta = models.IntegerField(default=0, verbose_name="Korea (CKFTA) Annex 14-A", blank=False)
    cufta = models.IntegerField(default=0, verbose_name="Ukraine (CUFTA) Annex 10-3", blank=False)
    wto_agp = models.IntegerField(default=0, verbose_name="WTO-AGP Canada Annex 1", blank=False)
    ceta = models.IntegerField(default=0, verbose_name="CETA Annex 19-4", blank=False)
    cptpp = models.IntegerField(default=0, verbose_name="CPTPP Chapter 15-A Section D", blank=False)
    cfta = models.IntegerField(default=0, verbose_name="CFTA Chapter 5", blank=False)

'''
Not Used
'''
# class GenericCodesModel(BooleanTradeAgreement):
#
#     gsin_class = models.CharField(max_length=12, default="", verbose_name="GSIN Class (4)")
#     gsin_code = models.CharField(max_length=12, default="", verbose_name="GSIN Code")
#     gsin_desc_en = models.CharField(max_length=128, default="", verbose_name="GSIN Code Description (English)")
#     gsin_desc_fr = models.CharField(max_length=128, default="", verbose_name="GSIN Code Description (Français)")
#     unspsc_code = models.CharField(max_length=12, default="", verbose_name="UNSPSC Code")
#     unspsc_code_desc_en = models.CharField(max_length=128, default="",
#                                            verbose_name="UNSPSC Code Description (English)")
#     unspsc_code_desc_fr = models.CharField(max_length=128, default="",
#                                            verbose_name="UNSPSC Code Description (Français)")
#
#     class Meta:
#         ordering = ['gsin_class', 'gsin_code']
#
#     def __str__(self):
#         return "{0} - {1}: {2}".format(self.gsin_class, self.gsin_code, self.gsin_desc_en)

'''
Commodity Type
'''
class CommodityType(models.Model):

    commodity_type = models.CharField(
        max_length=20,
        default='',
        verbose_name='Commodity Type'
    )

    def __str__(self):
        return self.name

'''
Two Goods Codes: FSC and UNSPSC
'''

class GoodsFscCode(BooleanTradeAgreement):

    commodity_type = models.ForeignKey(
        CommodityType,
        on_delete=models.SET_NULL,
        null = True
    )
    fsc_code = models.CharField(
        max_length=10,
        default='',
        verbose_name="Federal Supply Code"
    )
    fsc_code_desc = models.CharField(
        max_length=128,
        default="",
        verbose_name="Federal Supply Code Description"
    )

    class Meta:
        ordering = ['fsc_code', 'fsc_code_desc']
        unique_together = (('fsc_code', 'fsc_code_desc'),)

    def __str__(self):
        return "{0} - {1}".format(self.fsc_code, self.fsc_code_desc)


class GoodsUnspscCode(BooleanTradeAgreement):

    commodity_type = models.ForeignKey(
        CommodityType,
        on_delete=models.SET_NULL,
        null = True
    )

    unspsc_code = models.CharField(
        max_length=10,
        default='',
        verbose_name='United Nations Standard Produces and Services Code'
    )
    unspsc_code_desc = models.CharField(
        max_length=128,
        default='',
        verbose_name='United Nations Standard Products and Services Code Description'
    )

    class Meta:
        ordering = ['unspsc_code', 'unspsc_code_desc']
        unique_together = (('unspsc_code', 'unspsc_code_desc'))

    def __str__(self):
        return '{0} - {1}'.format(self.unspsc_code, self.unspsc_code_desc)


'''
Three Construction Codes: CCS, CPC, UNSPSC
'''
class ConstructionCcsCode(BooleanTradeAgreement):

    commodity_type = models.ForeignKey(
        CommodityType,
        on_delete=models.SET_NULL,
        null = True
    )

    ccs_code = models.CharField(
        max_length=10,
        default='',
        verbose_name='Common Classification System Code'
    )
    ccs_code_desc = models.CharField(
        max_length=128,
        default="",
        verbose_name="Common Classification System Description")

    class Meta:
        ordering = ['ccs_code', 'ccs_code_desc']
        unique_together = ('ccs_code', 'ccs_code_desc')

    def __str__(self):
        return "{0} - {1}".format(self.ccs_code, self.ccs_code_desc)


class ConstructionCpcCode(BooleanTradeAgreement):

    commodity_type = models.ForeignKey(
        CommodityType,
        on_delete=models.SET_NULL,
        null = True
    )

    cpc_code = models.CharField(
        max_length=8,
        default='',
        verbose_name='Central Product Classification Code'
    )
    cpc_code_desc = models.CharField(
        max_length=128,
        default='',
        verbose_name='Central Product Classification Code Description')

    class Meta:
        ordering = ['cpc_code', 'cpc_code_desc']
        unique_together = ('cpc_code', 'cpc_code_desc')

    def __str__(self):
        return '{0} - {1}'.format(self.cpc_code, self.cpc_code_desc)


class ConstructionUnspscCode(BooleanTradeAgreement):

    commodity_type = models.ForeignKey(
        CommodityType,
        on_delete=models.SET_NULL,
        null = True
    )

    unspsc_code = models.CharField(
        max_length=10,
        default='',
        verbose_name='United Nations Standard Products and Services Code')
    unspsc_code_desc = models.CharField(
        max_length=128,
        default='',
        verbose_name='United Nations Standard Products and Services Code Description')

    class Meta:
        ordering = ['unspsc_code', 'unspsc_code_desc']
        unique_together = ('unspsc_code', 'unspsc_code_desc')

    def __str__(self):
        return '{0} - {1}'.format(self.unspsc_code, self.unspsc_code_desc)


'''
Three Services Codes: CCS, CPC, UNSPSC
'''
class ServicesCcsCode(BooleanTradeAgreement):

    commodity_type = models.ForeignKey(
        CommodityType,
        on_delete=models.SET_NULL,
        null = True
    )

    ccs_code = models.CharField(
        max_length=12,
        default="",
        verbose_name="Common Classification System Code"
    )
    ccs_code_desc = models.CharField(
        max_length=128,
        default="",
        verbose_name="Common Classification System Code Description")

    class Meta:
        ordering = ['ccs_code', 'ccs_code_desc']
        unique_together = ('ccs_code', 'ccs_code_desc')

    def __str__(self):
        return "{0} - {1}".format(self.ccs_code, self.ccs_code_desc)


class ServicesCpcCode(BooleanTradeAgreement):

    commodity_type = models.ForeignKey(
        CommodityType,
        on_delete=models.SET_NULL,
        null = True
    )

    cpc_code = models.CharField(
        max_length=12,
        default='',
        verbose_name='Central Product Classification Code'
    )
    cpc_code_desc = models.CharField(
        max_length=128,
        default='',
        verbose_name='Central Product Classification Code Description'
    )

    class Meta:
        ordering = ['cpc_code', 'cpc_code_desc']
        unique_together = ('cpc_code', 'cpc_code_desc')

    def __str__(self):
        return '{0} -{1}'.format(self.cpc_code, self.cpc_code_desc)


class ServicesUnspscCode(BooleanTradeAgreement):

    commodity_type = models.ForeignKey(
        CommodityType,
        on_delete=models.SET_NULL,
        null = True
    )

    unspsc_code = models.CharField(
        max_length=10,
        default='',
        verbose_name='United Nations Standard Products and Services Code'
    )
    unspsc_code_desc = models.CharField(
        max_length=128,
        default='',
        verbose_name='United Nations Standard Products and Services Code Description'
    )

    class Meta:
        ordering = ['unspsc_code', 'unspsc_code_desc']
        unique_together = ('unspsc_code', 'unspsc_code_desc')

    def __str__(self):
        return '{0} - {1}'.format(self.unspsc_code, self.unspsc_code_desc)


'''
Limited Tendering Reasons
'''
class TenderingReason(BooleanTradeAgreement):

    desc_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")

    class Meta:
        unique_together = ('desc_en', 'desc_fr')

    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)


'''
Trade Agreement Exceptions
'''
class TAException(BooleanTradeAgreement):

    desc_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")

    class Meta:
        unique_together = ('desc_en', 'desc_fr')

    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)


'''
CFTA Exceptions
'''
class CftaException(BooleanTradeAgreement):

    desc_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")

    class Meta:
        unique_together = ('desc_en', 'desc_fr')

    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)


'''
Contract Value Thresholds
'''
class ValueThreshold(NumericTradeAgreements):

    desc_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")

    class Meta:
        unique_together = ('desc_en', 'desc_fr')

    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)


'''
Federal Entities
'''
class FederalEntities(BooleanTradeAgreement):

    name_en = models.TextField(default="-", unique=True, verbose_name="Name of Federal Entity (English)")
    name_fr = models.TextField(default="_", unique=True, verbose_name="Name of Federal Entity (Français)")

    class Meta:
        unique_together = ('name_en', 'name_fr')

    def __str__(self):
        return "{0} / {1}".format(self.name_en, self.name_fr)


'''
commodity code
'''
class CommodityCode(models.Model):
    commodity_code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

'''
Model Form
'''
class ModelGuide(models.Model):

    estimated_value = models.ForeignKey(ValueThreshold, on_delete=models.SET_NULL, null=True)
    federal_entities = models.ForeignKey(FederalEntities, on_delete=models.SET_NULL, null=True)
    commodity_type = models.ForeignKey(CommodityType, on_delete=models.SET_NULL, null=True)
    commodity_code = models.ForeignKey(CommodityCode, on_delete=models.SET_NULL, null=True)
    exceptions = models.ForeignKey(TAException, on_delete=models.SET_NULL, null=True)
    limited_tendering = models.ForeignKey(TenderingReason, on_delete=models.SET_NULL, null=True)
    cfta_ex = models.ForeignKey(CftaException, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
