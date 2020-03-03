from django.db import models

# TODO: Add validators

class BooleanTradeAgreement(models.Model):
    """
    This contains a boolean for each trade agreement
    """
    id = models.AutoField(primary_key=True)
    nafta_annex = models.BooleanField(
        default=False,
        verbose_name="NAFTA Annex 1001.1b-1",
        blank=False
    )
    ccfta = models.BooleanField(
        default=False,
        verbose_name="Chile (CCFTA) Annex K bis-01.1-3",
        blank=False
    )
    ccofta = models.BooleanField(
        default=False,
        verbose_name="Colombia (CCoFTA) Annex 1401-4",
        blank=False
    )
    chfta = models.BooleanField(
        default=False,
        verbose_name="Honduras (CHFTA) Annex 17.3",
        blank=False
    )
    cpafta = models.BooleanField(
        default=False,
        verbose_name="Panama (CPaFTA) Annex 4",
        blank=False
    )
    cpfta = models.BooleanField(
        default=False,
        verbose_name="Peru (CPFTA) Annex 1401. 1-3",
        blank=False
    )
    ckfta = models.BooleanField(
        default=False,
        verbose_name="Korea (CKFTA) Annex 14-A",
        blank=False
    )
    cufta = models.BooleanField(
        default=False,
        verbose_name="Ukraine (CUFTA) Annex 10-3",
        blank=False
    )
    wto_agp = models.BooleanField(
        default=False,
        verbose_name="WTO-AGP Canada Annex 1",
        blank=False
    )
    ceta = models.BooleanField(
        default=False,
        verbose_name="CETA Annex 19-4",
        blank=False
    )
    cptpp = models.BooleanField(
        default=False,
        verbose_name="CPTPP Chapter 15-A Section D",
        blank=False
    )
    cfta = models.BooleanField(
        default=False,
        verbose_name="CFTA Chapter 5",
        blank=False
    )

    class Meta:
        abstract=True

class NumericTradeAgreements(models.Model):
    """
    This gives every trade agreement a number field to use for value thresholds
    """
    id = models.AutoField(primary_key=True)
    nafta_annex = models.IntegerField(
        default=0,
        verbose_name="NAFTA Annex 1001.1b-1",
        blank=False
    )
    ccfta = models.IntegerField(
        default=0,
        verbose_name="Chile (CCFTA) Annex K bis-01.1-3",
        blank=False
    )
    ccofta = models.IntegerField(
        default=0,
        verbose_name="Colombia (CCoFTA) Annex 1401-4",
        blank=False
    )
    chfta = models.IntegerField(
        default=0,
        verbose_name="Honduras (CHFTA) Annex 17.3",
        blank=False
    )
    cpafta = models.IntegerField(
        default=0,
        verbose_name="Panama (CPaFTA) Annex 4",
        blank=False
    )
    cpfta = models.IntegerField(
        default=0,
        verbose_name="Peru (CPFTA) Annex 1401. 1-3",
        blank=False
    )
    ckfta = models.IntegerField(
        default=0,
        verbose_name="Korea (CKFTA) Annex 14-A",
        blank=False
    )
    cufta = models.IntegerField(
        default=0,
        verbose_name="Ukraine (CUFTA) Annex 10-3",
        blank=False
    )
    wto_agp = models.IntegerField(
        default=0,
        verbose_name="WTO-AGP Canada Annex 1",
        blank=False
    )
    ceta = models.IntegerField(
        default=0,
        verbose_name="CETA Annex 19-4",
        blank=False
    )
    cptpp = models.IntegerField(
        default=0,
        verbose_name="CPTPP Chapter 15-A Section D",
        blank=False
    )
    cfta = models.IntegerField(
        default=0,
        verbose_name="CFTA Chapter 5",
        blank=False
    )

    class Meta:
        abstract=True

class Entities(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has federal departments, agencies, ect...
    """
    name_en = models.CharField(
        max_length=128,
        default='',
        unique=True,
        verbose_name='Federal Entities'
    )
    name_fr = models.CharField(
        max_length=128,
        default='',
        unique=True,
        verbose_name='French Entities'
    )

    def __str__(self):
        return "{0} / {1}".format(self.name_en, self.name_fr)


class CommodityType(models.Model):
    commodity_type_en = models.CharField(
        max_length=128,
        default='',
        unique=True,
        verbose_name='Commodity Type EN'
    )
    commodity_type_fr = models.CharField(
        max_length=128,
        default='',
        unique=True,
        verbose_name='Commodity Type FR'
    )

    def __str__(self):
        return "{0} / {1}".format(self.commodity_type_en, self.commodity_type_fr)


class ValueThreshold(NumericTradeAgreements):
    """
    Subclass of :model: 'guide.NumericTradeAgreement'
    This class is for the dollar value thresholds in the trade agreements
    """
    type_value_en = models.ForeignKey(
        CommodityType,
        to_field='commodity_type_en',
        related_name='+',
        max_length=128,
        default='',
        verbose_name='Commodity Type EN',
        on_delete=models.CASCADE
    )
    type_value_fr = models.ForeignKey(
        CommodityType,
        to_field='commodity_type_fr',
        related_name='+',
        max_length=128,
        default='',
        verbose_name='Commodity Type FR',
        on_delete=models.CASCADE
    )
    name_en = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description (English)"
    )
    name_fr = models.TextField(
        default="_",
        unique=True,
        verbose_name="Description (Francais)"
    )

    def __str__(self):
        return "{0} / {1}".format(self.name_en, self.name_fr)



class CommodityCodeSystem(models.Model):
    commodity_code_system_en = models.CharField(
        max_length=128,
        default='',
        unique=True,
        verbose_name='Commodity Code System EN'
    )
    commodity_code_system_fr = models.CharField(
        max_length=128,
        default='',
        unique=True,
        verbose_name='Commodity Code System FR'
    )

    def __str__(self):
        return "{0} / {1}".format(self.commodity_code_system_en, self.commodity_code_system_fr)


class Code(models.Model):
    type_en = models.ForeignKey(
        CommodityType,
        to_field='commodity_type_en',
        related_name='+',
        max_length=128,
        default='',
        verbose_name='Commodity Type EN',
        on_delete=models.CASCADE,
        db_column='type_en'
    )
    type_fr = models.ForeignKey(
        CommodityType,
        to_field='commodity_type_fr',
        related_name='+',
        max_length=128,
        default='',
        verbose_name='Commodity Type FR',
        on_delete=models.CASCADE,
        db_column='type_fr'
    )
    code_system_en = models.ForeignKey(
        CommodityCodeSystem,
        to_field='commodity_code_system_en',
        related_name='+',
        max_length=128,
        default='',
        verbose_name='Commodity Code System EN',
        on_delete=models.CASCADE
    )
    code_system_fr = models.ForeignKey(
        CommodityCodeSystem,
        to_field='commodity_code_system_fr',
        related_name='+',
        max_length=128,
        default='',
        verbose_name='Commodity Code System FR',
        on_delete=models.CASCADE
    )

    code_en = models.CharField(
        max_length=20,
        default='',
        verbose_name='Code List EN',
        db_column='code_list_en'
    )
    code_fr = models.CharField(
        max_length=20,
        default='',
        verbose_name='Code List FR',
        db_column='code_list_fr'
    )

    def __str__(self):
        return "{0} / {1}".format(self.code_en, self.code_fr)


class TenderingReason(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has limited tendering reasons
    """
    name_en = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description (English)"
    )
    name_fr = models.TextField(
        default="_",
        unique=True,
        verbose_name="Description (Francais)"
    )

    def __str__(self):
        return "{0} / {1}".format(self.name_en, self.name_fr)


class TAException(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has trade agreement exceptions
    """
    name_en = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description (English)"
    )
    name_fr = models.TextField(
        default="_",
        unique=True,
        verbose_name="Description (Francais)"
    )

    def __str__(self):
        return "{0} / {1}".format(self.name_en, self.name_fr)


class CftaException(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has Canada Free Trade Agreement exceptions
    """
    name_en = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description (English)"
    )
    name_fr = models.TextField(
        default="_",
        unique=True,
        verbose_name="Description (Francais)"
    )

    def __str__(self):
        return "{0} / {1}".format(self.name_en, self.name_fr)





