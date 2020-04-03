from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import Entities, Code, TAException, TenderingReason, CftaException
from django.db.models import Q


class GuideFormEN(forms.Form):

    estimated_value = forms.IntegerField(
        label=_('Estimated Value'),
        required=True
    )
    estimated_value.widget.attrs['class'] = 'form-control required'

    entities = forms.ModelChoiceField(
        Entities.objects.filter(lang='EN').only('name'),
        label=_('Organization'),
        required=True
    )
    entities.widget.attrs['class'] = 'form-control'

    type = forms.CharField(
        label=_('Commodity Type'),
        required=True,
        widget = forms.Select()
    )
    type.widget.attrs['class'] = 'form-control'

    code_system = forms.CharField(
        widget = forms.Select(),
        label=_('Commodity Code System'),
        required=True
    )
    code_system.widget.attrs['class'] = 'form-control'


    code = forms.CharField(
        widget = forms.Select(),
        label=_('Commodity Code'),
        required=True
    )
    code.widget.attrs['class'] = 'form-control'



    exceptions = forms.ModelMultipleChoiceField(
        TAException.objects.filter(lang='EN').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Exceptions"),
        required=False
    )
    exceptions.widget.attrs['class'] = 'form-control'


    limited_tendering = forms.ModelMultipleChoiceField(
        TenderingReason.objects.filter(lang='EN').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Limited Tendering Reasons"),
        required=False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'

    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.filter(lang='EN').only('name'),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple,
        label=_("CFTA Exceptions"),
        required=False
    )
    cfta_exceptions.widget.attrs['class'] = 'form-control'

    def clean_type(self):
        # raise ValidationError('Construction isnt one')
        data = self.cleaned_data.get('type')
        if Code.objects.filter(type=data).exists():
            return data
        else:
            raise ValidationError('Invalid choice.  Please select a commodity type.')

    def clean_code_system(self):
        data = self.cleaned_data.get('code_system')
        if Code.objects.filter(code_system=data).exists():
            return data
        else:
            raise ValidationError('Invalid choice.  Please select a commodity code system')

    def clean_code(self):
        data = self.cleaned_data.get('code')
        if Code.objects.filter(code=data).exists():
            return data
        else:
            raise ValidationError('Invalid choice.  Please select a commodity code.')


class GuideFormFR(forms.Form):

    estimated_value = forms.IntegerField(
        label=_('Estimated Value'),
        required=True
    )
    estimated_value.widget.attrs['class'] = 'form-control required'

    entities = forms.ModelChoiceField(
        Entities.objects.filter(lang='FR').only('name'),
        label=_('Organization'),
        required=True
    )
    entities.widget.attrs['class'] = 'form-control'

    commodity_type = forms.ModelChoiceField(
        Code.objects.filter(lang='FR').only('type'),
        label=_('Commodity Type'),
        required=True
    )
    commodity_type.widget.attrs['class'] = 'form-control'

    commodity_system = forms.ModelChoiceField(
        Code.objects.filter(lang='FR').only('code_system'),
        label=_('Commodity Code System'),
        required=True
    )
    commodity_system.widget.attrs['class'] = 'form-control'

    commodity_code = forms.ModelChoiceField(
        Code.objects.filter(lang='FR').only('code'),
        label=_('Commodity Code'),
        required=True
    )
    commodity_type.widget.attrs['class'] = 'form-control'

    exceptions = forms.ModelMultipleChoiceField(
        TAException.objects.filter(lang='FR').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Exceptions"),
        required=False
    )
    exceptions.widget.attrs['class'] = 'form-control'

    limited_tendering = forms.ModelMultipleChoiceField(
        TenderingReason.objects.filter(lang='FR').only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Limited Tendering Reasons"),
        required=False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'

    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.filter(lang='FR').only('name'),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple,
        label=_("CFTA Exceptions"),
        required=False
    )
    cfta_exceptions.widget.attrs['class'] = 'form-control'
