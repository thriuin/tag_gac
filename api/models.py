from django.db import models

# TODO: Add validators
class BilingualClass(models.Model):
    """
    Subclass of models.Model
    This class is for bilingual labels
    """
    class Meta:
        abstract = True

    def __str__(self):
        return "{0} / {1}".format(self.name_en, self.name_fr)


class BooleanTradeAgreement(BilingualClass):
    """
    Subclass of :model: 'guide.BilingualClass'
    This contains a boolean for each trade agreement
    """
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


class NumericTradeAgreements(BilingualClass):
    """
    Subclass of :model: 'guide.BilingualClass'
    This gives every trade agreement a number field to use for value thresholds
    """
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


class Entities(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has federal departments, agencies, ect...
    """
    name_en = models.CharField(max_length=128, default='', verbose_name='Federal Entities')
    name_fr = models.CharField(max_length=128, default='', verbose_name='French Entities')


class ValueThreshold(NumericTradeAgreements):
    """
    Subclass of :model: 'guide.NumericTradeAgreement'
    This class is for the dollar value thresholds in the trade agreements
    """
    name_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    name_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")


class CommodityCodeSystem(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class is for the different commodity coding systems (UNSPSC, FSC, ect...)
    """
    name_en = models.CharField(max_length=128, default='', verbose_name='Commodity Code System')
    name_fr = models.CharField(max_length=128, default='', verbose_name='French Commodity coding system')

class CodeList(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class is for the codes with the foreign key for the relevant code system
    """
    fk = models.ForeignKey(CommodityCodeSystem, on_delete=models.CASCADE)
    name_en = models.CharField(max_length=20, default='', verbose_name='Code List')
    name_fr = models.CharField(max_length=20, default='', verbose_name='Code List FR')


class TenderingReason(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has limited tendering reasons
    """
    name_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    name_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")


class TAException(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has trade agreement exceptions
    """
    name_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    name_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")


class CftaException(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has Canada Free Trade Agreement exceptions
    """
    name_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    name_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")
