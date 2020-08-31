from guide.forms import RequiredFieldsForm, GeneralExceptionForm, LimitedTenderingForm, CftaExceptionForm
import guide.models as models
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from guide.models import AGREEMENTS, AGREEMENTS_FIELDS

FORMS = [("0", RequiredFieldsForm),
         ("1", GeneralExceptionForm),
         ("2", CftaExceptionForm),
         ("3", LimitedTenderingForm)]

TEMPLATES = {"0": "mandatory_elements.html",
             "1": "exceptions.html",
             "2": "cfta_exceptions.html",
             "3": "limited_tendering.html"}

url_name='guide:form_step'
done_step_name='guide:done_step'

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def organization_rule(agreement, data):
    """Checks which trade agreements apply to the selected entity

    Arguments:
        context {dictionary} -- The context keeps track of all the values submitted and the analysis
        org_name {string} -- From context this gets the submitted value

    Raises:
        ValueError: Returns value error if there is a problem with context

    Returns:
        [dictionary] -- Returns updated context dict with analysis (true or false)
    """
    org = data['entities']

    for k in agreement.keys():
        check = models.Organization.objects.filter(name=org).values_list(k).get()[0]
        agreement[k]['entities'] = check

    return agreement


def value_threshold_rule(agreement, data):
    """Checks whether the value submitted by the user is less than or greater than the
    value in the trade agreement.

    Arguments:
        context {dictionary} -- The context keeps track of all the values submitted and the analysis
        col_estimated_value {string} -- From context this gets the submitted value
        col_type {string} -- From context this gets the submitted value

    Raises:
        ValueError: Output if there is an error with the context

    Returns:
        [dictionary] -- Updates context with the analyzed value, either true or false
    """
    model = models.ValueThreshold
    value = int(data['estimated_value'])
    type = data['type']
    try:
        for k in agreement.keys():
            threshold = model.objects.filter(type=type).values_list(k).get()[0]
            if value < threshold:
                agreement[k]['estimated_value'] = False
            else:
                agreement[k]['estimated_value'] = True
    except:
        raise ValueError
    return agreement

def code_rule(agreement, data_dict):
    """Checks if the code selected by the user is covered by each trade agreement.

    Arguments:
        context {dictionary} -- Context tracks user input and analysis
        col_code {string} -- String to select user value for code from the context
        type_col {string} -- String to select user value for type from the context
        org_name {string} -- String to select user value for org from the context

    Raises:
        ValueError: If error in context

    Returns:
        [dictionary] -- Returns context with updated analysis
    """
    code = data_dict['code']
    commodity = data_dict['type']
    org = data_dict['entities']
    code_db = models.Code.objects.filter(code=code)


    def construction_coverage(_agreement):
        if models.ConstructionCoverage.objects.filter(org_fk=org).exists():
            for k in agreement.keys():
                check = models.ConstructionCoverage.objects.filter(org_fk=org).values_list(k).get()[0]
                if check:
                    _agreement[k]['code'] = False
        else:
            for k in _agreement.keys():
                check = code_db.values_list(k).get()[0]
                if not check:
                    _agreement[k]['code'] = False
        return _agreement
    
    def goods_coverage(_agreement):
        if models.GoodsCoverage.objects.filter(org_fk=org).exists():
            for k in _agreement.keys():
                check = code_db.values_list(k).get()[0]
                if not check:
                    _agreement[k]['code'] = False
        return _agreement

    def services_coverage(_agreement):
        for k in _agreement.keys():
            check = code_db.values_list(k).get()[0]
            if not check:
                _agreement[k]['code'] = False
        return _agreement
    
    def code_org_exclusion(_agreement):
        if models.CodeOrganizationExclusion.objects.filter(org_fk=org).filter(code_fk=code).exists():
            for k in _agreement.keys():
                check = code_db.values_list(k).get()[0]
                if not check:
                    _agreement[k]['code'] = False
        return _agreement

    def set_false(_agreement):
        if str(commodity) == 'Goods':
            _agreement = goods_coverage(_agreement)
        elif str(commodity) == 'Services':
            _agreement = services_coverage(_agreement)
        else:
            _agreement = construction_coverage(_agreement)
        _agreement = code_org_exclusion(_agreement)
        return _agreement

    def set_true(_agreement):
        for k in _agreement.keys():
            try: 
                _test = _agreement[k]['code']
            except:
                _agreement[k]['code'] = True
        return _agreement

    agreement = set_false(agreement)
    agreement = set_true(agreement)
    return agreement



def exceptions_rule(agreement, data, exception):
    """This function goes through the exceptions that the user selected and checks which trade agreements
    apply to each exception.  If a user selects a trade agreements and an exception applies then that
    agreement is set to False.
    Arguments:
        context {dictionary} -- Context tracks user input and analysis
        col {[type]} -- From context this gets the submitted value
        model {model} -- This gets the model related to the submitted value
    Raises:
        ValueError: If error in context
    Returns:
        Dictionary -- Returns updated context dictionary with analysis
    """
    def set_false(_agreement, _exception, _model, _exception_name):
        for k in _agreement.keys():
            for ex in _exception:
                check = _model.objects.filter(name=ex).values_list(k).get()[0]
                if check:
                    _agreement[k][_exception_name] = False
        return _agreement

    def set_true(_agreement, _exception_name):
        for k in _agreement.keys():
            try: 
                _test = _agreement[k][_exception_name]
            except:
                _agreement[k][_exception_name] = True
        return _agreement

    try:
        for exception_name, model in exception.items():
            exception = data[exception_name]
            if exception:
                agreement = set_false(agreement, exception, model, exception_name)
            agreement = set_true(agreement, exception_name)
    except:
        pass

    return agreement

