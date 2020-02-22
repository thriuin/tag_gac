from django import forms
from django.utils.translation import ugettext_lazy as _
import re
from api.models import Entities, ValueThreshold, \
    CommodityCodeSystem, CodeList, TenderingReason, TAException, CftaException


class MainForm(forms.Form):
    '''
    Value threshold form :model: 'guide.ValueThreshold'
    Entities form :model: 'guide.Entities'
    CommodityCodeSystem form :model: 'guide.CommodityCodeSystem'
    CodeList form :model: 'guide.CodeList'
    TenderingReason form :model: 'guide.TenderingReason'
    TAException form :model: 'guide.TAException'
    CftaException form :model: 'guide.CftaException'
    '''
    value_threshold = forms.IntegerField(
        label=_('Estimated Value'),
        min_value=0,
        required=True
    )
    value_threshold.widget.attrs['class'] = 'form-control required'

    entities = forms.ModelChoiceField(
        Entities.objects.all(),
        to_field_name='id',
        label=_('Federal Entities'),
        required=True
    )
    entities.widget.attrs['class'] = 'form-control required'

    commodity_code_system = forms.ModelChoiceField(
        CommodityCodeSystem.objects.all(),
        to_field_name = 'id',
        label = _('Commodity Code System'),
        required = True
    )
    commodity_code_system.widget.attrs['class'] = 'form-control required'

    code_list = forms.ModelChoiceField(
        CodeList.objects.all(),
        to_field_name = 'id',
        label = _('Code List'),
        required=True,
        disabled = True
    )
    code_list.widget.attrs['class'] = 'form-control required'

    tendering_reason = forms.ModelMultipleChoiceField(
        queryset=TenderingReason.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_('Limited Tendering Reason'),
        required=False
    )
    tendering_reason.widget.attrs['class'] = 'form-control required'

    ta_exception = forms.ModelMultipleChoiceField(
        queryset=TAException.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_('Trade Agreement Exceptions'),
        required=False
    )
    ta_exception.widget.attrs['class'] = 'form-control required'

    cfta_exception = forms.ModelMultipleChoiceField(
        queryset=CftaException.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_('Canada Free Trade Agreement Exceptions'),
        required=False
    )
    cfta_exception.widget.attrs['class'] = 'form-control required'

    def clean_code_list(self):
        return re.sub('\D', '', self.cleaned_date.get('code_list'))
