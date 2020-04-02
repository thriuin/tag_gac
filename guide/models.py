from django.db import models

# TODO: Add validators


class Language(models.Model):
    CHOICES = [
        ('EN', 'English'),
        ('FR', 'Francais')
    ]
    lang = models.CharField(
        choices=CHOICES,
        default='',
        verbose_name='Select Language Field',
        blank=False,
        max_length=2
        )


    class Meta:
        abstract=True


class BooleanTradeAgreement(Language):
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
    name = models.CharField(
        max_length=128,
        default='',
        unique=True,
        verbose_name='Entities'
    )
    tc = models.BooleanField(
        default=False,
        verbose_name='Department of Transport',
        blank=False
    )
    weapons_rule = models.BooleanField(
        default=False,
        verbose_name='Defence RCMP or CCG',
        blank=False
    )

    def __str__(self):
        return self.name


class CommodityType(Language):
    commodity_type = models.CharField(
        max_length=128,
        default='',
        unique=True,
        verbose_name='Commodity Type'
    )


    class Meta:
        unique_together = ['commodity_type', 'lang']

    def __str__(self):
        return self.commodity_type


class ValueThreshold(NumericTradeAgreements):
    """
    Subclass of :model: 'guide.NumericTradeAgreement'
    This class is for the dollar value thresholds in the trade agreements
    """
    type_value = models.ForeignKey(
        CommodityType,
        to_field='commodity_type',
        related_name='+',
        max_length=128,
        default='',
        verbose_name='Commodity Type',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.type_value.commodity_type


class Code(BooleanTradeAgreement):
    type = models.ForeignKey(
        CommodityType,
        to_field='commodity_type',
        related_name='+',
        max_length=128,
        default='',
        verbose_name='Commodity Type',
        on_delete=models.CASCADE
    )

    code = models.CharField(
        max_length=128,
        default='',
        verbose_name='Code List',
        db_column='code_list'
    )

    def __str__(self):
        return self.code



class TenderingReason(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has limited tendering reasons
    """
    name = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description"
    )

    def __str__(self):
        return self.name



class TAException(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has trade agreement exceptions
    """
    name = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description"
    )
    def __str__(self):
        return self.name

class CftaException(BooleanTradeAgreement):
    """
    Subclass of :model: 'guide.BooleanTradeAgreement'
    This class has Canada Free Trade Agreement exceptions
    """
    name = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description"
    )

    def __str__(self):
        return self.name


class Instructions(Language):
    name = models.TextField(
        default='-',
        unique=True,
        verbose_name='Instructions'
    )

    def __str__(self):
        return self.name





