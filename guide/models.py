from django.db import models

# TODO: Add validators


class Language(models.Model):
    """
    This facilitates the app being bilingual.  This base model is inherited by the following models:
    :model:`guide.BooleanTradeAgreement`,
    :model:`guide.NumericTradeAgreement`,
    :model:`guide.CommodityType`
    """
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
    This model has a True/False for each trade agreement.
    This model inherits from :model:'guide.Language'
    This model is inherited by the following models:
    :model:`guide.Entities`
    :model:`guide.Code`
    :model:`guide.TenderingReason`
    :model:`guide.TAException`
    :model:`guide.CftaException`
    """
    id = models.AutoField(primary_key=True)
    nafta = models.BooleanField(
        default=False,
        verbose_name="NAFTA",
        blank=False
    )
    ccfta = models.BooleanField(
        default=False,
        verbose_name="CCFTA",
        blank=False
    )
    ccofta = models.BooleanField(
        default=False,
        verbose_name="CCoFTA",
        blank=False
    )
    chfta = models.BooleanField(
        default=False,
        verbose_name="CHFTA",
        blank=False
    )
    cpafta = models.BooleanField(
        default=False,
        verbose_name="CPaFTA",
        blank=False
    )
    cpfta = models.BooleanField(
        default=False,
        verbose_name="CPFTA",
        blank=False
    )
    ckfta = models.BooleanField(
        default=False,
        verbose_name="CKFTA",
        blank=False
    )
    cufta = models.BooleanField(
        default=False,
        verbose_name="CUFTA",
        blank=False
    )
    wto_agp = models.BooleanField(
        default=False,
        verbose_name="WTO-AGP",
        blank=False
    )
    ceta = models.BooleanField(
        default=False,
        verbose_name="CETA",
        blank=False
    )
    cptpp = models.BooleanField(
        default=False,
        verbose_name="CPTPP",
        blank=False
    )
    cfta = models.BooleanField(
        default=False,
        verbose_name="CFTA",
        blank=False
    )

    class Meta:
        abstract=True


class NumericTradeAgreement(models.Model):
    """
    This gives every trade agreement a number field to use for value thresholds
    This is inherited by :model:`guide.ValueThreshold`
    """
    id = models.AutoField(primary_key=True)
    nafta = models.IntegerField(
        default=0,
        verbose_name="NAFTA",
        blank=False
    )
    ccfta = models.PositiveIntegerField(
        default=0,
        verbose_name="CCFTA",
        blank=False
    )
    ccofta = models.PositiveIntegerField(
        default=0,
        verbose_name="CCoFTA",
        blank=False
    )
    chfta = models.PositiveIntegerField(
        default=0,
        verbose_name="CHFTA",
        blank=False
    )
    cpafta = models.PositiveIntegerField(
        default=0,
        verbose_name="CPaFTA",
        blank=False
    )
    cpfta = models.PositiveIntegerField(
        default=0,
        verbose_name="CPFTA",
        blank=False
    )
    ckfta = models.PositiveIntegerField(
        default=0,
        verbose_name="CKFTA",
        blank=False
    )
    cufta = models.PositiveIntegerField(
        default=0,
        verbose_name="CUFTA",
        blank=False
    )
    wto_agp = models.PositiveIntegerField(
        default=0,
        verbose_name="WTO-AGP",
        blank=False
    )
    ceta = models.PositiveIntegerField(
        default=0,
        verbose_name="CETA",
        blank=False
    )
    cptpp = models.PositiveIntegerField(
        default=0,
        verbose_name="CPTPP",
        blank=False
    )
    cfta = models.PositiveIntegerField(
        default=0,
        verbose_name="CFTA",
        blank=False
    )

    class Meta:
        abstract=True


class Organization(BooleanTradeAgreement):
    """
    Subclass of :model:`guide.BooleanTradeAgreement`
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
    goods_rule = models.BooleanField(
        default=False,
        verbose_name='Defence RCMP or CCG',
        blank=False
    )

    def __str__(self):
        return self.name


class CommodityType(Language):
    '''
    Inherits from :model:`guide.Language`
    This is for Goods, Services, Construction
    '''
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


class ValueThreshold(NumericTradeAgreement):
    """
    Subclass of :model:`guide.NumericTradeAgreement`
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
        return str(self.type_value)


class Code(BooleanTradeAgreement):
    '''
    Inherits from :model:`guide.BooleanTradeAgreement`
    Foreign key from :model:`guide.CommodityType`
    This combines commodity types with specific commodity codes.
    '''
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
    Subclass of :model:`guide.BooleanTradeAgreement`
    This class has limited tendering reasons
    """
    name = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description"
    )

    def __str__(self):
        return self.name


class GeneralException(BooleanTradeAgreement):
    """
    Subclass of :model:`guide.BooleanTradeAgreement`
    This class has trade agreement exceptions
    """
    name = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description"
    )
    def __str__(self):
        return self.name

    # def get_fields(self):
    #     return [field.name for field in GeneralException._meta.fields]


class CftaException(BooleanTradeAgreement):
    """
    Subclass of :model:`guide.BooleanTradeAgreement`
    This class has Canada Free Trade Agreement exceptions
    """
    name = models.TextField(
        default="-",
        unique=True,
        verbose_name="Description"
    )

    def __str__(self):
        return self.name


# class TradeAgreement(Language):
#     name = models.CharField(
#         default='',
#         unique=True,
#         verbose_name = 'Trade Agreement',
#         max_length = 100
#     )


