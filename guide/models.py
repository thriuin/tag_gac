from django.db import models
from django.utils.translation import gettext_lazy as _


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
        verbose_name = _('CCFTA'),
        blank = False
    )
    ccofta = models.BooleanField(
        default = False,
        verbose_name = _('CCoFTA'),
        blank = False
    )
    chfta = models.BooleanField(
        default = False,
        verbose_name = _('CHFTA'),
        blank = False
    )
    cpafta = models.BooleanField(
        default = False,
        verbose_name = _('CPaFTA'),
        blank = False
    )
    cpfta = models.BooleanField(
        default = False,
        verbose_name = _('CPFTA'),
        blank = False
    )
    ckfta = models.BooleanField(
        default = False,
        verbose_name = _('CKFTA'),
        blank = False
    )
    cufta = models.BooleanField(
        default = False,
        verbose_name = _('CUFTA'),
        blank = False
    )
    wto_agp = models.BooleanField(
        default = False,
        verbose_name = _('WTO-AGP'),
        blank = False
    )
    ceta = models.BooleanField(
        default = False,
        verbose_name = _('CETA'),
        blank = False
    )
    cptpp = models.BooleanField(
        default = False,
        verbose_name = _('CPTPP'),
        blank = False
    )
    cfta = models.BooleanField(
        default = False,
        verbose_name = _('CFTA'),
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

    def __str__(self):
        return self.name


class CommodityType(models.Model):
    '''
    Inherits from :model:`guide.Language`
    This is for Goods, Services, Construction
    '''
    commodity_type = models.CharField(
        max_length = 128,
        default = '',
        unique = True,
        verbose_name = _('Commodity Type')
    )


    class Meta:
        ordering = ['commodity_type']

    def __str__(self):
        return self.commodity_type


class Code(BooleanTradeAgreement):
    '''
    Inherits from :model:`guide.BooleanTradeAgreement`
    Foreign key from :model:`guide.CommodityType`
    This combines commodity types with specific commodity codes.
    '''
    type = models.ForeignKey(
        CommodityType,
        to_field = 'commodity_type',
        related_name = '+',
        max_length = 128,
        default = '',
        verbose_name = _('Commodity Type'),
        on_delete = models.CASCADE
    )

    code = models.CharField(
        max_length = 128,
        default = '',
        verbose_name = _('Code List'),
        db_column = 'code_list'
    )

    def __str__(self):
        return self.code


class OrganizationWithCommodityTypeRules(models.Model):
    com_type = models.ForeignKey(
        CommodityType,
        to_field = 'commodity_type',
        related_name = '+',
        max_length = 128,
        default = '',
        verbose_name = _('Commodity Type'),
        on_delete = models.CASCADE
    )
    tc = models.BooleanField(
        default = False,
        verbose_name = _('Department of Transport has a specific commodity coverage for Construction Services'),
        blank = False
    )
    goods_rule = models.BooleanField(
        default = False,
        verbose_name = _('The Department of National Defence, the Canadian Coast Guard, and the Royal Canadian Mounted Police have specific commodity code coverage for goods.'),
        blank = False
    )

    def __str__(self):
        return str(self.com_type)


class OrganizationWithCommodityCodeRules(models.Model):
    code_fk = models.ForeignKey(
        Code,
        to_field = 'code',
        related_name = '+',
        max_length = 250,
        default = '',
        verbose_name = _('Code FK'),
        on_delete = models.CASCADE
    )
    org_fk = models.ForeignKey(
        Organization,
        to_field = 'name',
        related_name = '+',
        max_length = 250,
        default = '',
        verbose_name = _('Org FK'),
        on_delete = models.CASCADE
    )


class ValueThreshold(models.Model):
    """
    Subclass of :model:`guide.NumericTradeAgreement`
    This class is for the dollar value thresholds in the trade agreements
    """
    id = models.AutoField(primary_key = True)
    ccfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CCFTA'),
        blank = False
    )
    ccofta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CCoFTA'),
        blank = False
    )
    chfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CHFTA'),
        blank = False
    )
    cpafta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CPaFTA'),
        blank = False
    )
    cpfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CPFTA'),
        blank = False
    )
    ckfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CKFTA'),
        blank = False
    )
    cufta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CUFTA'),
        blank = False
    )
    wto_agp = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('WTO-AGP'),
        blank = False
    )
    ceta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CETA'),
        blank = False
    )
    cptpp = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CPTPP'),
        blank = False
    )
    cfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = _('CFTA'),
        blank = False
    )

    type_value = models.ForeignKey(
        CommodityType,
        to_field = 'commodity_type',
        related_name = '+',
        max_length = 128,
        default = '',
        verbose_name = _('Commodity Type'),
        on_delete = models.CASCADE
    )

    def __str__(self):
        return str(self.type_value)


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
