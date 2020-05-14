from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import Organization, Code, GeneralException, TenderingReason, CftaException

class MandatoryElementsEN(forms.Form):

    estimated_value = forms.IntegerField(
        label=_('What is the total estimated value of the procurement?'),
        required=True
    )
    estimated_value.widget.attrs['class'] = 'form-control'

    entities = forms.ModelChoiceField(
        Organization.objects.filter(lang='EN').only('name'),
        label=_('Who is the procuring entity?'),
        required=True
    )
    entities.widget.attrs['class'] = 'form-control'

    type = forms.CharField(
        label=_('What is the procurement commodity type?'),
        required=True,
        widget = forms.Select()
    )
    type.widget.attrs['class'] = 'form-control'
    code = forms.CharField(
        widget = forms.Select(),
        label=_('What is the trade agreement commodity code most closely associated with the procurement?'),
        required=True
    )
    code.widget.attrs['class'] = 'form-control'

    def clean_type(self):
        type = self.cleaned_data.get('type')
        if Code.objects.filter(type=type).exists():
            return type
        else:
            raise ValidationError('Invalid choice.  Please select a commodity type.')

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Code.objects.filter(code=code).exists():
            return code
        else:
            raise ValidationError('Invalid choice.  Please select a commodity code.')

class ExceptionsEN(forms.Form):

    exceptions = forms.ModelMultipleChoiceField(
        GeneralException.objects.filter(lang='EN').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Exceptions"),
        required=False
    )
    exceptions.widget.attrs['class'] = 'form-control'


class LimitedTenderingEN(forms.Form):

    limited_tendering = forms.ModelMultipleChoiceField(
        TenderingReason.objects.filter(lang='EN').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Limited Tendering Reasons"),
        required=False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'


class CftaExceptionsEN(forms.Form):

    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.filter(lang='EN').only('name'),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple,
        label=_("CFTA Exceptions"),
        required=False
    )
    cfta_exceptions.widget.attrs['class'] = 'form-control'


