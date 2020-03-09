from django.db import models


class BooleanTradeAgreement(models.Model):

    id = models.AutoField(primary_key=True)
    nafta = models.BooleanField(default=False, verbose_name="NAFTA Annex 1001.1b-1", blank=False)
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
    cfta = models.BooleanField(default=False, verbose_name="Canadian Free Trade Agreement (CFTA)", blank=True)


class NumericTradeAgreements(models.Model):

    id = models.AutoField(primary_key=True)
    nafta = models.IntegerField(default=0, verbose_name="NAFTA Annex 1001.1b-1", blank=False)
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
    cfta = models.BooleanField(default=False, verbose_name="Canadian Free Trade Agreement (CFTA)", blank=True)


class TextTradeAgreements(models.Model):

    id = models.AutoField(primary_key=True)
    nafta = models.TextField(default='', verbose_name="NAFTA Article 1016")
    ccfta = models.TextField(default='', verbose_name="Chile (CCFTA) Annex K bis-09")
    ccofta = models.TextField(default='', verbose_name="Colombia (CCoFTA) Annex 1409")
    chfta = models.TextField(default='', verbose_name="Honduras (CHFTA) Annex 17.11")
    cpafta = models.TextField(default='', verbose_name="Panama (CPaFTA) Article 16.10")
    cpfta = models.TextField(default='', verbose_name="Peru (CPFTA) Article 1409")
    ckfta = models.TextField(default='', verbose_name="Korea (CKFTA) Article 14.3 (WTO)")
    cufta = models.TextField(default='', verbose_name="Ukraine (CUFTA) Annex 10-3")
    wto_agp = models.TextField(default='', verbose_name="WTO-AGP Article XV ")
    ceta = models.TextField(default='', verbose_name="CETA 19.12")
    cptpp = models.TextField(default='', verbose_name="CPTPP  Article 15.10 (2)")
    cfta = models.TextField(default='', verbose_name="Canadian Free Trade Agreement (CFTA)")


class CommodityTypes(models.Model):
    
    type_en = models.CharField(max_length=128, default="-", unique=True, verbose_name="Commodity Type (English)")
    type_fr = models.CharField(max_length=128, default="_", unique=True, verbose_name="Commodity Type (Français)")
    
    def __str__(self):
        return "{0} / {1}".format(self.type_en, self.type_fr)


class CommodityCodingSystem(models.Model):

    system_en = models.CharField(max_length=128, default="-", unique=True, verbose_name="Commodity Code System (English)")
    system_fr = models.CharField(max_length=128, default="_", unique=True, verbose_name="Commodity Code System (Français)")
    
    def __str__(self):
        return "{0} / {1}".format(self.system_en, self.system_fr)
        

class CommodityCode(BooleanTradeAgreement):
    
    commodity_type_en = models.ForeignKey(CommodityTypes, to_field="type_en", related_name="+", 
        max_length=128, default="-", verbose_name="Commodity Type Foreign Field (English)", 
        on_delete=models.CASCADE)

    commodity_type_fr = models.ForeignKey(CommodityTypes, to_field="type_fr", related_name="+",
        max_length=128, default="_", verbose_name="Commodity Type Foreign Field (Français)", 
        on_delete=models.CASCADE)

    commodity_code_system_en = models.ForeignKey(CommodityCodingSystem, to_field="system_en", related_name="+", 
        max_length=128, default="-", verbose_name="Commodity Code System Foreign Field (English)", 
        on_delete=models.CASCADE)

    commodity_code_system_fr = models.ForeignKey(CommodityCodingSystem, to_field="system_fr", related_name="+", 
        max_length=128, default="-", verbose_name="Commodity Code System Foreign Field (Français)", 
        on_delete=models.CASCADE)

    commodity_code_en = models.CharField(max_length=128, default="-", unique=True, verbose_name="Commodity Code System (English)")
    commodity_code_fr = models.CharField(max_length=128, default="-", unique=True, verbose_name="Commodity Code System (Français)")

    def __str__(self):
        return "{0} / {1}".format(self.commodity_code_en, self.commodity_code_fr)


class Entities(BooleanTradeAgreement):
    desc_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")

    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)


class TenderingReason(BooleanTradeAgreement):

    desc_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")

    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)


class TAException(BooleanTradeAgreement):

    desc_en = models.TextField(default="-", unique=True, verbose_name="Description (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Description (Français)")
   
    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)

    class Meta:
        unique_together = (('desc_en', 'desc_fr'),)


class ValueThreshold(NumericTradeAgreements):

    type_value_en = models.ForeignKey(CommodityTypes, to_field='type_en', related_name='+', max_length=128, 
        default='', verbose_name='Commodity Type Value Field (English)', on_delete=models.CASCADE)

    type_value_fr = models.ForeignKey(CommodityTypes, to_field='type_fr', related_name='+', max_length=128, 
        default='', verbose_name='Commodity Type Value Field (Français)', on_delete=models.CASCADE)

    def __str__(self):
        return "{0} / {1}".format(self.type_value_en, self.type_value_fr)


class CftaExceptions(TextTradeAgreements):

    desc_en = models.TextField(default="-", unique=True, verbose_name="Reason (English)")
    desc_fr = models.TextField(default="_", unique=True, verbose_name="Reason (Français)")

    def __str__(self):
        return "{0} / {1}".format(self.desc_en, self.desc_fr)


class TAUrls(models.Model):

    ta_id = models.TextField(default="-", unique=True, verbose_name="Trade Agreement")
    url_en = models.TextField(default="-", unique=True, verbose_name="URL (English)")
    url_fr = models.TextField(default="-", unique=True, verbose_name="URL (Français)")

