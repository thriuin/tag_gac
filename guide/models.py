from django.db import models


class GenericTradeAgreements(models.Model):

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


class GenericCodesModel(GenericTradeAgreements):

    gsin_class = models.CharField(max_length=12, default="", verbose_name="GSIN Class (4)")
    gsin_code = models.CharField(max_length=12, default="", verbose_name="GSIN Code")
    gsin_desc_en = models.CharField(max_length=128, default="", verbose_name="GSIN Code Description (English)")
    gsin_desc_fr = models.CharField(max_length=128, default="", verbose_name="GSIN Code Description (Français)")
    unspsc_code = models.CharField(max_length=12, default="", verbose_name="UNSPSC Code")
    unspsc_code_desc_en = models.CharField(max_length=128, default="",
                                           verbose_name="UNSPSC Code Description (English)")
    unspsc_code_desc_fr = models.CharField(max_length=128, default="",
                                           verbose_name="UNSPSC Code Description (Français)")

    class Meta:
        ordering = ['gsin_class', 'gsin_code']

    def __str__(self):
        return "{0} - {1}: {2}".format(self.gsin_class, self.gsin_code, self.gsin_desc_en)


class GoodsCodes(GenericTradeAgreements):

    fs_code = models.CharField(max_length=10, default='', verbose_name="Federal Supply Code")
    fs_code_desc = models.CharField(max_length=128, default="", verbose_name="Federal Supply Code Description")

    class Meta:
        ordering = ['fs_code', 'fs_code_desc']
        unique_together = (('fs_code', 'fs_code_desc'),)

    def __str__(self):
        return "{0} - {1}".format(self.fs_code, self.fs_code_desc)


class ConstructionCodes(GenericTradeAgreements):

    fs_code = models.CharField(max_length=10, default='', verbose_name="Federal Supply Code")
    fs_code_desc = models.CharField(max_length=128, default="", verbose_name="Federal Supply Code Description")

    def __str__(self):
        return "{0} - {1}".format(self.fs_code, self.fs_code_desc)


class ServicesCodes(GenericTradeAgreements):

    nafta_code = models.CharField(max_length=12, default="",
                                  verbose_name="NAFTA Common Classification System Codes - Groups")
    ccs_level_2 = models.CharField(max_length=12, default="",
                                   verbose_name="NAFTA Common Classification System Codes - Sub-group")
    gsin_class = models.CharField(max_length=12, default="", verbose_name="GSIN Class (4)")
    desc_en = models.CharField(max_length=128, default="", verbose_name="Code Description")

    class Meta:
        ordering = ['nafta_code', 'ccs_level_2', 'gsin_class']
        unique_together = (('nafta_code', 'ccs_level_2', 'gsin_class'),)

    def __str__(self):
        return "{0} - {1}".format(self.ccs_level_2, self.gsin_class)

class TenderingReasons(GenericTradeAgreements):

    desc_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")

    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)