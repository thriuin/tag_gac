from django.db import models
from django.utils.translation import gettext_lazy as _

TYPE_CHOICES = [('1', 'GOODS'), 
                ('2', 'SERVICES'), 
                ('3', 'CONSTRUCTION')]

AGREEMENTS = (
    _('CCFTA'), 
    _('CCoFTA'), 
    _('CHFTA'), 
    _('CPaFTA'), 
    _('CPFTA'), 
    _('CKFTA'), 
    _('CUFTA'), 
    _('WTO-AGP'),
    _('CETA'), 
    _('CPTPP'), 
    _('CFTA')
)

AGREEMENTS_FIELDS = [field.replace('-', '_').lower() for field in AGREEMENTS]

class BooleanTradeAgreement(models.Model):
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
    ccfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[0],
        blank = False
    )
    ccofta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[1],
        blank = False
    )
    chfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[2],
        blank = False
    )
    cpafta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[3],
        blank = False
    )
    cpfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[4],
        blank = False
    )
    ckfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[5],
        blank = False
    )
    cufta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[6],
        blank = False
    )
    wto_agp = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[7],
        blank = False
    )
    ceta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[8],
        blank = False
    )
    cptpp = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[9],
        blank = False
    )
    cfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[10],
        blank = False
    )


    class Meta:
        abstract = True


class Organization(BooleanTradeAgreement):
    """
    Subclass of :model:`guide.BooleanTradeAgreement`
    This class has federal departments, agencies, ect...
    """
    name = models.CharField(
        max_length = 250,
        default = '',
        unique = True,
        verbose_name = _('Entities')
    )


    class Meta:
        ordering = ['name']
        verbose_name_plural = "  Entities" # 2 space
    
    def __str__(self):
        return self.name


class CommodityType(models.Model):
    '''
    Inherits from :model:`guide.Language`
    This is for Goods, Services, Construction
    '''
    c_type = models.CharField(
        choices=TYPE_CHOICES,
        max_length = 128,
        default = '',
        unique = True,
        verbose_name = _('Commodity Type')
    )
    commodity_type = models.CharField(
        max_length = 128,
        default = '',
        unique = True,
        verbose_name = _('Commodity Type')
    )


    class Meta:
        ordering = ['commodity_type']
        verbose_name_plural = "  Commodity Types" # 2 space
 
    def __str__(self):
        return self.commodity_type


class Code(BooleanTradeAgreement):
    '''
    Inherits from :model:`guide.BooleanTradeAgreement`
    Foreign key from :model:`guide.CommodityType`
    This combines commodity types with specific commodity codes.
    '''
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(
        CommodityType,
        to_field = 'commodity_type',
        related_name = '+',
        verbose_name = _('Commodity Type'),
        on_delete = models.CASCADE
    )
    code = models.CharField(
        max_length = 128,
        default = '',
        unique = True,
        verbose_name = _('Code')
    )

    def __str__(self):
        return self.code
    class Meta:
        verbose_name_plural = " Commodity Codes" # 1 space


class ConstructionCoverage(BooleanTradeAgreement):

    org_fk = models.ForeignKey(
        Organization,
        to_field = 'name',
        related_name = '+',
        verbose_name = _('Org fk en ca'),
        on_delete = models.CASCADE
    )


    class Meta:
        verbose_name_plural = "Construction Coverage" # 0 space


class GoodsCoverage(BooleanTradeAgreement):
    
    org_fk = models.ForeignKey(
        Organization,
        to_field = 'name',
        related_name = '+',
        verbose_name = _('Org fk en ca'),
        on_delete = models.CASCADE
    )

    def __str__(self):
        return str(self.org_fk)
    
    class Meta:
        verbose_name_plural = "Goods Coverage" # 0 space

class CodeOrganizationExclusion(BooleanTradeAgreement):
    code_fk = models.ForeignKey(
        Code,
        to_field = 'code',
        related_name = '+',
        verbose_name = _('Code FK en ca'),
        on_delete = models.CASCADE
    )
    org_fk = models.ForeignKey(
        Organization,
        to_field = 'name',
        related_name = '+',
        verbose_name = _('Org fk en ca'),
        on_delete = models.CASCADE
    )

    def __str__(self):
        return f"{self.org_fk} - {self.code_fk} - Exclusion"

    class Meta:
        verbose_name_plural = "Commodity Code - Entities - Exclusions" # 0 space


class ValueThreshold(models.Model):
    """
    Subclass of :model:`guide.NumericTradeAgreement`
    This class is for the dollar value thresholds in the trade agreements
    """
    id = models.AutoField(primary_key = True)
    ccfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[0],
        blank = False
    )
    ccofta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[1],
        blank = False
    )
    chfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[2],
        blank = False
    )
    cpafta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[3],
        blank = False
    )
    cpfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[4],
        blank = False
    )
    ckfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[5],
        blank = False
    )
    cufta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[6],
        blank = False
    )
    wto_agp = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[7],
        blank = False
    )
    ceta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[8],
        blank = False
    )
    cptpp = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[9],
        blank = False
    )
    cfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[10],
        blank = False
    )

    type = models.ForeignKey(
        CommodityType,
        to_field = 'commodity_type',
        related_name = '+',
        max_length = 128,
        default = '',
        verbose_name = _('Commodity Type'),
        on_delete = models.CASCADE
    )

    def __str__(self):
        return str(self.type)
    class Meta:
        verbose_name_plural = "  Value Thresholds" # 2 space


class LimitedTenderingReason(BooleanTradeAgreement):
    """
    Subclass of :model:`guide.BooleanTradeAgreement`
    This class has limited tendering reasons
    """
    name = models.TextField(
        default = '',
        unique = True,
        verbose_name = _('Description')
    )

    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name_plural = "  Limited Tendering Reasons" # 2 space


class GeneralException(BooleanTradeAgreement):
    """
    Subclass of :model:`guide.BooleanTradeAgreement`
    This class has trade agreement exceptions
    """
    name = models.TextField(
        default = '',
        unique = True,
        verbose_name = _('Description')
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "  General Exceptions" # 2 space


class CftaException(BooleanTradeAgreement):
    """
    Subclass of :model:`guide.BooleanTradeAgreement`
    This class has Canada Free Trade Agreement exceptions
    """
    name = models.TextField(
        default = '',
        unique = True,
        verbose_name = _('Description')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "  CFTA Exceptions" # 2 space