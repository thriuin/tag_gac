from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import CommodityType, \
    GoodsFscCode, GoodsUnspscCode,\
    ServicesCcsCode, ServicesCpcCode, ServicesUnspscCode, \
    ConstructionCcsCode, ConstructionCpcCode, ConstructionUnspscCode, \
    CftaException, TenderingReason, TAException, FederalEntities


class GuideForm(forms.Form):

    estimated_value = forms.IntegerField(
        label=_('Estimated Value'),
        min_value=0,
        required=True
    )
    estimated_value.widget.attrs['class'] = 'form-control required'

    organization = forms.ModelChoiceField(
        queryset=FederalEntities.objects.all(),
        label='Organization',
        required=True
    )
    organization.widget.attrs['class'] = 'form-control'


    commodity_type = forms.ModelChoiceField(
        queryset = CommodityType.objects.all(),
        label=_('Commodity Type'),
        required=True,
        initial=''
    )
    commodity_type.widget.attrs['class'] = 'form-control'

    '''
    Two goods codes: FSC, UNSPSC
    '''
    goods_fsc_codes = forms.ModelChoiceField(
        queryset = GoodsFscCode.objects.all(),
        to_field_name="id",
        label=_('Goods FSC Codes'),
        required=False
        )
    goods_fsc_codes.widget.attrs['class'] = 'form-control'

    goods_unspsc_codes = forms.ModelChoiceField(
        queryset=GoodsUnspscCode.objects.all(),
        to_field_name="id",
        label=_('Goods UNSPSC Codes'),
        required=False
    )
    goods_unspsc_codes.widget.attrs['class'] = 'form-control'
    '''
    Three services codes: CCS, CPC, UNSPSC
    '''
    services_ccs_codes = forms.ModelChoiceField(
        queryset = ServicesCcsCode.objects.all(),
        to_field_name="id",
        required=False,
        label=_("CCS Codes")
        )
    services_ccs_codes.widget.attrs['class'] = 'form-control'

    services_cpc_codes = forms.ModelChoiceField(
        queryset = ServicesCpcCode.objects.all(),
        to_field_name="id",
        required=False,
        label=_("CPC Codes")
        )
    services_cpc_codes.widget.attrs['class'] = 'form-control'

    services_unspsc_codes = forms.ModelChoiceField(
        queryset = ServicesUnspscCode.objects.all(),
        to_field_name="id",
        required=False,
        label=_("UNSPSC Codes")
        )
    services_unspsc_codes.widget.attrs['class'] = 'form-control'

    '''
    Three construction codes: CCS, CPC, UNSPSC
    '''
    construction_ccs_code = forms.ModelChoiceField(
        queryset=ConstructionCcsCode.objects.all(),
        to_field_name="id",
        required=False,
        label=_("CCS Codes")
        )
    construction_ccs_code.widget.attrs['class'] = 'form-control'

    construction_cpc_code = forms.ModelChoiceField(
        queryset=ConstructionCpcCode.objects.all(),
        to_field_name="id",
        required=False,
        label=_("CPC Codes")
        )
    construction_cpc_code.widget.attrs['class'] = 'form-control'

    construction_unspsc_code = forms.ModelChoiceField(
        queryset=ConstructionUnspscCode.objects.all(),
        to_field_name="id",
        required=False,
        label=_("UNSPSC Codes")
        )
    construction_unspsc_code.widget.attrs['class'] = 'form-control'

    '''
    Solicitation Procedure
    '''
    solicitation = forms.ChoiceField(
        label=_('Solicitation Procedure'),
        choices=(('tc', _('Traditional Competitive')),
              ('ob', _('Open Bidding')),
              ('ss', _('Sole Source')))
    )
    solicitation.widget.attrs['class'] = 'form-control'

    exemptions = forms.ModelMultipleChoiceField(
        queryset = TAException.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_("Exceptions"),
        required=False
    )
    exemptions.widget.attrs['class'] = 'form-control'

    limited_tendering = forms.ModelMultipleChoiceField(
        queryset = TenderingReason.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_("Limited Tendering Reasons"),
        required=False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'

    cfta_exceptions = forms.ModelMultipleChoiceField(
        queryset = CftaException.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="CFTA Exceptions",
        required=False
    )
    cfta_exceptions.widget.attrs['class'] = 'form-control'

    def clean_commodity_type(self):
        '''
        Provide a custom validation for the commodity type select field. Whatever commodity type is selected the
        corresponding goods, services, or construction select field must have a selected item.
        :return: A ValidationError if the corresponding commodity is not selected.
        '''
        if self.cleaned_data['commodity_type'] == 'goods':
            if 'goods_codes' not in self.data or self.data['goods_codes'] is None:
                raise ValidationError(
                    _('Select a good from the list below'),
                    code='invalid',
                )
            try:
                code = int(self.data['goods_codes'])
            except:
                raise ValidationError(
                    _('Select a good from the list below'),
                    code='invalid',
                )
        elif self.cleaned_data['commodity_type'] == 'services':
            if 'services_codes' not in self.data or self.data['services_codes'] is None:
                raise ValidationError(
                    _('Select a service from the list below'),
                    code='invalid',
                )
            try:
                code = int(self.data['services_codes'])
            except:
                raise ValidationError(
                    _('Select a service from the list below'),
                    code='invalid',
                )
        elif self.cleaned_data['commodity_type'] == 'construction':
            if 'construction_code' not in self.data or self.data['construction_code'] is None:
                raise ValidationError(
                    _('Select a construction from the list below'),
                    code='invalid',
                )
            try:
                code = int(self.data['construction_code'])
            except:
                raise ValidationError(
                    _('Select a construction from the list below'),
                    code='invalid',
                )

