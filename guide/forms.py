from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import CommodityTypes, CommodityCodingSystem, CommodityCode, TAException, TenderingReason, CftaExceptions, Entities


class GuideForm(forms.Form):

    estimated_value = forms.IntegerField(label=_('Estimated Value'), min_value=0, required=True)
    estimated_value.widget.attrs['class'] = 'form-control required'

    entities = forms.ModelChoiceField(Entities.objects.all(), to_field_name="id",
                                    label=_('Organization'),
                                     required=True)
    entities.widget.attrs['class'] = 'form-control'

    commodity_type = forms.ModelChoiceField(CommodityTypes.objects.all(), to_field_name="id",
                                        label=_('Commodity Type'),
                                       required=True)
    commodity_type.widget.attrs['class'] = 'form-control'

    commodity_code_system = forms.ModelChoiceField(CommodityCodingSystem.objects.all(), to_field_name="id",
                                                    label=_('Commodity Code System'),
                                                    required=True)
    commodity_code_system.widget.attrs['class'] = 'form-control'

    commodity_code = forms.ModelChoiceField(CommodityCode.objects.all(), to_field_name="id",
                                            label=_('Commodity Code'),
                                            required=True)
    commodity_code.widget.attrs['class'] = 'form-control'

    limited_tendering = forms.ModelMultipleChoiceField(TenderingReason.objects.all(),
                                                         to_field_name="id", required=False,
                                                         label=_("Limited Tendering Reasons"),
                                                         widget=forms.CheckboxSelectMultiple)
    limited_tendering.widget.attrs['class'] = 'form-control'

    exemptions = forms.ModelMultipleChoiceField(TAException.objects.all(),
                                                 to_field_name="id", required=False,
                                                 label=_("Trade Agreement Exemptions"),
                                                 widget=forms.CheckboxSelectMultiple)

    exemptions.widget.attrs['class'] = 'form-control'
    
    cfta_exceptions = forms.ModelMultipleChoiceField(CftaExceptions.objects.all(),
                                                        to_field_name="id", required=False,
                                                        label=_("CFTA Exceptions"),
                                                        widget=forms.CheckboxSelectMultiple)
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

