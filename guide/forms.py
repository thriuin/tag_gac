from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import Organization, Code, GeneralException, TenderingReason, CftaException

estimated_value_label = _('What is the total estimated value of the procurement? ')
entities_label = _('Who is the procuring entity?')
type_label = _('What is the procurement commodity type?')
code_label = _('What is the Goods and Services Identification Number commodity (GSIN) code most closely associated with the procurement?')
general_exceptions_label = _("Exceptions")
limited_tendering_label = _("Limited Tendering Reasons")
cfta_exceptions_label = _("CFTA Exceptions")

class RequiredFieldsFormEN(forms.Form):

    estimated_value = forms.IntegerField(
        label=estimated_value_label,
        required=True,
        min_value=0
    )
    estimated_value.widget.attrs['class'] = 'form-control'

    entities = forms.ModelChoiceField(
        Organization.objects.filter(lang='EN').only('name'),
        label=entities_label,
        required=True
    )
    entities.widget.attrs['class'] = 'form-control'

    type = forms.CharField(
        label=type_label,
        required=True,
        widget = forms.Select()
    )
    type.widget.attrs['class'] = 'form-control'
    code = forms.CharField(
        widget = forms.Select(),
        label=code_label,
        required=True
    )
    code.widget.attrs['class'] = 'form-control'

    def clean_type(self):
        type = self.cleaned_data.get('type')
        if Code.objects.filter(type=type).exists():
            return type
        else:
            raise ValidationError('Select a valid choice. That choice is not one of the available choices.')

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Code.objects.filter(code=code).exists():
            return code
        else:
            raise ValidationError('Select a valid choice. That choice is not one of the available choices.')

class GeneralExceptionFormEN(forms.Form):

    exceptions = forms.ModelMultipleChoiceField(
        GeneralException.objects.filter(lang='EN').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=general_exceptions_label,
        required=False
    )
    exceptions.widget.attrs['class'] = 'form-control'


class LimitedTenderingFormEN(forms.Form):

    limited_tendering = forms.ModelMultipleChoiceField(
        TenderingReason.objects.filter(lang='EN').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=limited_tendering_label,
        required=False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'


class CftaExceptionFormEN(forms.Form):

    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.filter(lang='EN').only('name'),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple,
        label=cfta_exceptions_label,
        required=False
    )
    cfta_exceptions.widget.attrs['class'] = 'form-control'


