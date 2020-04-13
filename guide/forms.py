from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import Entities, Code, TAException, TenderingReason, CftaException
from django.db.models import Q



class MandatoryElementsEN(forms.Form):

    estimated_value = forms.IntegerField(
        label=_('Estimated Value'),
        required=True
    )
    estimated_value.widget.attrs['class'] = 'form-control'

    entities = forms.ModelChoiceField(
        Entities.objects.filter(lang='EN').only('name'),
        label=_('Organization'),
        required=True
    )
    entities.widget.attrs['class'] = 'form-control'

    type = forms.CharField(
        label=_('Commodity Type'),
        required=False,
        widget = forms.Select()
    )
    type.widget.attrs['class'] = 'form-control'

    code = forms.CharField(
        widget = forms.Select(),
        label=_('Commodity Code'),
        required=False
    )
    code.widget.attrs['class'] = 'form-control'
    


class ExceptionsEN(forms.Form):
    prefix = ''
    exceptions = forms.ModelMultipleChoiceField(
        TAException.objects.filter(lang='EN').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Exceptions"),
        required=False
    )
    exceptions.widget.attrs['class'] = 'form-control'


class LimitedTenderingEN(forms.Form):
    prefix = ''
    limited_tendering = forms.ModelMultipleChoiceField(
        TenderingReason.objects.filter(lang='EN').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Limited Tendering Reasons"),
        required=False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'


class CftaExceptionsEN(forms.Form):
    prefix = ''
    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.filter(lang='EN').only('name'),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple,
        label=_("CFTA Exceptions"),
        required=False
    )
    cfta_exceptions.widget.attrs['class'] = 'form-control'


