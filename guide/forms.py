from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import GoodsCode, ConstructionCode, ServicesCode, TAException, LimitedTendering


class GuideForm(forms.Form):

    estimated_value = forms.IntegerField(label=_('Estimated Value'), min_value=0, required=True)
    estimated_value.widget.attrs['class'] = 'form-control required'

    organization = forms.ChoiceField(label='Organization',
                                     choices=(('tbs-sct', _('Treasury Board Secretariat')),
                                              ('pco', _('Privy Council Office'))),
                                     required=True)
    organization.widget.attrs['class'] = 'form-control'

    commodity_type = forms.ChoiceField(label=_('Commodity Type'),
                                       choices=(('goods', _('Goods')),
                                                ('services', _('Services')),
                                                ('construction', _('Construction'))),
                                       required=True,
                                       initial='goods')
    commodity_type.widget.attrs['class'] = 'form-control'

    goods_codes = forms.ModelChoiceField(GoodsCode.objects.all(), to_field_name="id",
                                         label=_('Goods Codes'),
                                         required=False)
    goods_codes.widget.attrs['class'] = 'form-control'

    services_codes = forms.ModelChoiceField(ServicesCode.objects.all(),
                                            to_field_name="id",
                                            required=False,
                                            label=_("Service Codes"))
    services_codes.widget.attrs['class'] = 'form-control'

    construction_code = forms.ModelChoiceField(ConstructionCode.objects.all(),
                                               to_field_name="id",
                                               required=False,
                                               label=_("Construction Codes"))
    construction_code.widget.attrs['class'] = 'form-control'

    solicitation = forms.ChoiceField(label=_('Solicitation Procedure'),
                                     choices=(('tc', _('Traditional Competitive')),
                                              ('ob', _('Open Bidding')),
                                              ('ss', _('Sole Source'))))
    solicitation.widget.attrs['class'] = 'form-control'

    exemptions = forms.ModelMultipleChoiceField(TAException.objects.all(),
                                                 to_field_name="id", required=False,
                                                 label=_("Trade Agreement Exemptions"),
                                                 widget=forms.CheckboxSelectMultiple)

    exemptions.widget.attrs['class'] = 'form-control'

    limited_tendering = forms.ModelMultipleChoiceField(LimitedTendering.objects.all(),
                                                         to_field_name="id", required=False,
                                                         label=_("Limited Tendering Reasons"),
                                                         widget=forms.CheckboxSelectMultiple)
    limited_tendering.widget.attrs['class'] = 'form-control'

    cfta_exceptions = forms.MultipleChoiceField(
        choices=(
            ("1", "Measures necessary to protect intellectual property, provided that the measures are not applied in a manner that would constitute a means of arbitrary or unjustifiable discrimination between Parties where the same conditions prevail or are a disguised restriction on trade;"),
            ("2", "Procurement or acquisition of: \
            (i) fiscal agency or depository services; \
            (ii) liquidation and management services for regulated financial institutions; or \
            (iii) services related to the sale, redemption, and distribution of public debt, including l oans and government bonds, notes, and other securities;"),
            ("3", "Procurement of financial services respecting the management of government financial assets and liabilities \(i.e. treasury operations\), including ancillary advisory and information services,  whether or not delivered by a financial institution;"),
            ("4", "Procurement of health services or social services"),
            ("5", "Procurement of services that may, under applicable law, only be provided by licensed lawyers or notaries"),
            ("6", "Procurement of services of expert witnesses or factual witnesses used in court or legal proceedings"),
            ("7", "Procurement of goods or services from philanthropic institutions, non-profit organizations, prison labour, or natural persons with disabilities "),
            ("8", "Procurement of goods or services  conducted for the specific purpose of providing international assistance, including development aid, provided that the procuring entity does not discriminate on the basis of origin or location within Canada of goods, services, or suppliers"),
            ("9", "Procurement of goods or services conducted: \
            (A) under the particular procedure or condition of an international agreement relating to the stationing of troops or relating to the joint implementation by the signatory countries of a project; \
            (B) under the particular procedure or condition of an international organisation, or funded by international grants, loans, or other assistance, if the procedure or condition would be inconsistent with this Chapter.")
        ),
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

