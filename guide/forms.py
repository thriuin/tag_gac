from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import Organization, Code, GeneralException, LimitedTenderingReason, CftaException, CommodityType
from dal import autocomplete

estimated_value_label = _('What is the total estimated value of the procurement? ')
entities_label = _('Who is the procuring entity?')
type_label = _('What is the procurement commodity type?')
code_label = _('What is the Goods and Services Identification Number commodity (GSIN) code most closely associated with the procurement?')
general_exceptions_label = _("Exceptions")
limited_tendering_label = _("Limited Tendering Reasons")
cfta_exceptions_label = _("CFTA Exceptions")

estimated_value_error = 'Please enter a valid number greater than zero.'
generic_error = 'Select a valid choice. That choice is not one of the available choices.'


class RequiredFieldsForm(forms.Form):
    """[summary]

    Args:
        forms ([type]): [description]

    Raises:
        ValidationError: [description]
        ValidationError: [description]
        ValidationError: [description]
        ValidationError: [description]
        ValidationError: [description]

    Returns:
        [type]: [description]
    """
    estimated_value = forms.IntegerField(
        label = estimated_value_label,
        required = True,
        min_value = 0
    )
    estimated_value.widget.attrs['class'] = 'form-control'

    entities = forms.ModelChoiceField(
        Organization.objects.all(),
        label = entities_label,
        required = True,
        widget=autocomplete.ModelSelect2(url='guide:entities_autocomplete', attrs={'class':'form-control'})
    )

    type = forms.ModelChoiceField(
        CommodityType.objects.all(),
        label = type_label,
        required = True,
        widget = autocomplete.ModelSelect2(url='guide:type_autocomplete', attrs={'class':'form-control'})
    )

    code = forms.ModelChoiceField(
        Code.objects.only('code').all(),
        label = code_label,
        required = False,
        widget = autocomplete.ModelSelect2(url = 'guide:code_autocomplete', forward=['type'], attrs={'class':'form-control', 'size': '1'})
    )

    # def clean_estimated_value(self):
    #     val = self.cleaned_data.get('estimated_value')
    #     if val is None:
    #         raise ValidationError(estimated_value_error)
    #     else:
    #         return int(val)

    # def clean_entities(self):
    #     clean_org = self.cleaned_data.get('entities')
    #     if Organization.objects.filter(name = clean_org).exists():
    #         return clean_org
    #     else:
    #         raise ValidationError(generic_error)

    # def clean_type(self):
    #     clean_type = self.cleaned_data.get('type')
    #     if CommodityType.objects.filter(commodity_type = clean_type).exists():
    #         return clean_type
    #     else:
    #         raise ValidationError(generic_error)

    # def clean_code(self):
    #     code = self.cleaned_data.get('code')
    #     if Code.objects.filter(code = code).exists():
    #         return code
    #     else:
    #         raise ValidationError(generic_error)

class GeneralExceptionForm(forms.Form):
    """[summary]

    Args:
        forms ([type]): [description]
    """
    exceptions = forms.ModelMultipleChoiceField(
        GeneralException.objects.only('name'),
        to_field_name = 'id',
        widget = forms.CheckboxSelectMultiple,
        label = general_exceptions_label,
        required = False
    )
    exceptions.widget.attrs['class'] = 'form-control'


class LimitedTenderingForm(forms.Form):
    """[summary]

    Args:
        forms ([type]): [description]
    """
    limited_tendering = forms.ModelMultipleChoiceField(
        LimitedTenderingReason.objects.only('name'),
        to_field_name = 'id',
        widget = forms.CheckboxSelectMultiple,
        label = limited_tendering_label,
        required = False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'


class CftaExceptionForm(forms.Form):
    """[summary]

    Args:
        forms ([type]): [description]
    """
    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.only('name'),
        to_field_name = 'id',
        widget = forms.CheckboxSelectMultiple,
        label = cfta_exceptions_label,
        required = False
    )



