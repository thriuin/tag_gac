from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import GoodsOGDCode, GoodsMilitaryCode, ConstructionCode, ServicesCode


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

    goods_codes = forms.ModelChoiceField(GoodsOGDCode.objects.all(), to_field_name="id",
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

    exemptions = forms.MultipleChoiceField(
        choices=(('1', _("Shipbuilding and repair (applies to all agreements except the CFTA)")),
                 ('2', _("Services procured in support of military forces located overseas (applies to all agreements)")),
                 ('3', _("Contracts respecting Federal Supply Classification (FSC) 58 (communications detection and coherent radiation equipment) (applies to all agreements except for the CFTA)")),
                 ('4', _("Set-asides for small businesses (other than indigenous businesses) (applies to all agreements except for CETA)")),
                 ('5', _("Agricultural products made in furtherance of agricultural support programs or human feeding programs (applies to all agreements except for CFTA)")),
                 ('6', _("Procurements respecting FSC 70 74 and 36 for the Department of Transport (applies to all agreements except for the CFTA CUFTA CKFTA WTO-AGP CETA and CPTPP)")),
                 ('7', _("FSC 70 74 and 36 for the Department of Heritage (in respect to those functions that were formerly the responsibility of the Department of Communications) (applies to all agreements except for the CFTA CUFTA CKFTA WTO-AGP CETA and CPTPP)")),
                 ('8', _("Indigenous Businesses set-aside (applies to all agreements)")),
                 ('9', _("Measures necessary to protect public morals order or safety (applies to all agreements)")),
                 ('10', _("Measures necessary to protect human animal or plant life or health (applies to all agreements)")),
                 ('11', _("Measures necessary to protect intellectual property (applies to all agreements)")),
                 ('12', _("Measures relating to goods or services of persons with disabilities philanthropic institutions or prison labour (applies to all agreements)")),
                 ('13', _("Procurement of goods or services from not-for-profit institutions (applies to all agreements except for CETA and CPTPP)")),
                 ('14', _("Procurement related to an international crossing between Canada and another country (applies to all agreements except for NAFTA CCFTA CCoFTA CHFTA CPaFTA and CPFTA)")),
                 ('15', _("Related to space projects for the Canadian Space Agency (applies to CFTA only)")),
                 ('16', _("Procurements for the Canadian Space Agency other than for satellite communications earth observation and global navigation satellite systems (applies to CETA only)"))),
        widget=forms.CheckboxSelectMultiple,
        label=_("Exceptions"),
        required=False
    )
    exemptions.widget.attrs['class'] = 'form-control'

    limited_tendering = forms.MultipleChoiceField(
        choices=(
            ("1", "None"),
            ("2", "No response to bid solicitation or no suppliers applied to participate in the procurement"),
            ("3", "No tenders conformed to the essential requirements of the tender documentation"),
            ("4", "The tenders submitted were collusive"),
            ("5", "Goods or services can be supplied by only a particular supplier"),
            ("6", "Work of art"),
            ("7", "Patent protection or copyright"),
            ("8", "Absence of competition for technical reasons"),
            ("9", "Economic or technical reasons, such as Interchangeable Parts"),
            ("10", "Additional deliveries by original supplier if a change in supplier would cause duplication of "
                   "costs or significant inconvenience"),
            ("11", "Goods purchased on a commodities market"),
            ("12", "Procurement of a Prototype"),
            ("13", "Extreme urgency"),
            ("14", "Exceptionally advantageous (not CPaFTA)S"),
            ("15", "Winner of an architectural design contest"),
            ("16", "Consulting services regarding matters of a confidential nature (Does not apply to CPTPP, CETA, "
                   "WTO-GAP, CKFTA, CUFTA)"),
            ("17", "Additional construction services (only for CPaFTA and CPTPP, CCFTA)")
        ),
        widget=forms.CheckboxSelectMultiple,
        label=_("Limited Tendering Reasons"),
        required=False
    )
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

