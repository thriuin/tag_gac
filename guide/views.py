from django.shortcuts import render
from guide.models import Code, GeneralException, CftaException, LimitedTenderingReason, Organization, CommodityType, ValueThreshold, GoodsCoverage, ConstructionCoverage, CodeOrganizationExclusion
from guide.forms import RequiredFieldsForm, GeneralExceptionForm, LimitedTenderingForm, CftaExceptionForm
from formtools.wizard.views import NamedUrlCookieWizardView
from django.http import HttpResponse
from dal import autocomplete
from django.views.generic import View
from guide.models import AGREEMENTS_FIELDS
import json
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

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

def create_data_dict(self, forms):
    """[summary]

    Args:
        forms ([type]): [description]

    Returns:
        [type]: [description]
    """
    func_data_dict = {}
    try:
        for f in forms:
            func_data_dict.update(self.get_cleaned_data_for_step(f))
    except:
        pass
    return func_data_dict

def get_coverage(data_dict):
    """[summary]

    Args:
        data_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    def create_agreement_dict():
        """[summary]

        Returns:
            [type]: [description]
        """
        func_agreement_dict = {k:{} for k in AGREEMENTS_FIELDS}
        return func_agreement_dict
    
    def value_threshold_rule(agreement, data):
        """[summary]

        Args:
            agreement ([type]): [description]
            data ([type]): [description]

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]
        """
        model = ValueThreshold
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
            pass
        return agreement

    def organization_rule(agreement, data):
        """[summary]

        Args:
            agreement ([type]): [description]
            data ([type]): [description]

        Returns:
            [type]: [description]
        """
        org = data['entities']

        for k in agreement.keys():
            check = Organization.objects.filter(name=org).values_list(k).get()[0]
            agreement[k]['entities'] = check

        return agreement

    def code_rule(agreement, data_dict):
        """[summary]

        Args:
            agreement ([type]): [description]
            data_dict ([type]): [description]

        Returns:
            [type]: [description]
        """
        code = data_dict['code']
        commodity = data_dict['type']
        org = data_dict['entities']
        code_db = Code.objects.filter(code=code)


        def construction_coverage(_agreement):
            """[summary]

            Args:
                _agreement ([type]): [description]

            Returns:
                [type]: [description]
            """
            if ConstructionCoverage.objects.filter(org_fk=org).exists():
                for k in agreement.keys():
                    check = ConstructionCoverage.objects.filter(org_fk=org).values_list(k).get()[0]
                    if check:
                        _agreement[k]['code'] = False
            else:
                for k in _agreement.keys():
                    check = code_db.values_list(k).get()[0]
                    if not check:
                        _agreement[k]['code'] = False
            return _agreement
        
        def goods_coverage(_agreement):
            """[summary]

            Args:
                _agreement ([type]): [description]

            Returns:
                [type]: [description]
            """
            if GoodsCoverage.objects.filter(org_fk=org).exists():
                for k in _agreement.keys():
                    check = code_db.values_list(k).get()[0]
                    if not check:
                        _agreement[k]['code'] = False
            return _agreement

        def services_coverage(_agreement):
            """[summary]

            Args:
                _agreement ([type]): [description]

            Returns:
                [type]: [description]
            """
            for k in _agreement.keys():
                check = code_db.values_list(k).get()[0]
                if not check:
                    _agreement[k]['code'] = False
            return _agreement
        
        def code_org_exclusion(_agreement):
            """[summary]

            Args:
                _agreement ([type]): [description]

            Returns:
                [type]: [description]
            """
            if CodeOrganizationExclusion.objects.filter(org_fk=org).filter(code_fk=code).exists():
                for k in _agreement.keys():
                    check = code_db.values_list(k).get()[0]
                    if not check:
                        _agreement[k]['code'] = False
            return _agreement

        def set_false(_agreement):
            """[summary]

            Args:
                _agreement ([type]): [description]

            Returns:
                [type]: [description]
            """
            print
            if str(commodity) == 'Goods':
                _agreement = goods_coverage(_agreement)
            elif str(commodity) == 'Services':
                _agreement = services_coverage(_agreement)
            else:
                _agreement = construction_coverage(_agreement)
            _agreement = code_org_exclusion(_agreement)
            return _agreement

        def set_true(_agreement):
            """[summary]

            Args:
                _agreement ([type]): [description]

            Returns:
                [type]: [description]
            """
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
        """[summary]

        Args:
            agreement ([type]): [description]
            data ([type]): [description]
            exception ([type]): [description]
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

    def determine_final_coverage(_agreement):
        """[summary]

        Args:
            _agreement ([type]): [description]

        Returns:
            [type]: [description]
        """
        cxt={k:True if all(_agreement[k].values()) else False for k in _agreement.keys()}
        return cxt

    agreement_dict = create_agreement_dict()

    agreement_dict = value_threshold_rule(agreement_dict, data_dict)
    agreement_dict = organization_rule(agreement_dict, data_dict)
    agreement_dict = code_rule(agreement_dict, data_dict)

    exception_dict = {
        'exceptions': GeneralException,
        'cfta_exceptions': CftaException,
    }
    agreement_dict = exceptions_rule(agreement_dict, data_dict, exception_dict)
    
    data_dict['ta'] = agreement_dict
    data_dict['bool'] = determine_final_coverage(agreement_dict)
    return data_dict

def get_output_text(_output_text):
    """[summary]

    Args:
        _output_text ([type]): [description]
    """
    def get_ta_text(_ta_text):
        """[summary]

        Args:
            _ta_text ([type]): [description]

        Returns:
            [type]: [description]
        """
        if sum(_ta_text['bool'].values()) == 0:
            output = 'No trade agreements apply.  '
        else:
            output = ''
            for k, v in _ta_text['bool'].items():
                if v is True:
                    output = output + k.upper() + ', '
        _ta_text['output'] = output[:-2]
        return _ta_text

    def get_summary_text(_sum_text):
        """[summary]

        Args:
            _sum_text ([type]): [description]

        Returns:
            [type]: [description]
        """
        _sum_text2 = {k:['None'] if not v else v for k,v in _sum_text.items()}
        if 'limited_tendering' in _sum_text2:
            pass
        else:
            _sum_text2['limited_tendering'] = ['None']
        return _sum_text2

    def get_tables_text(_table_text):
        """[summary]

        Args:
            _table_text ([type]): [description]

        Returns:
            [type]: [description]
        """
        _table_text['tables'] = {}
        for k1, v1 in _table_text['ta'].items():
            k1 = k1.upper()
            _table_text['tables'][k1] = {}
            for k2, v2 in v1.items():
                if k2 == 'type' or k2 == 'limited_tendering':
                    pass
                else:
                    k2 = k2.replace('_', ' ')
                    k2 = k2.title()
                    if k1 == 'CFTA':
                        k2 = k2.replace('Cfta Exceptions', 'CFTA Exceptions')
                        _table_text['tables'][k1][k2] = v2
                    else:
                        if k2 == 'Cfta Exceptions':
                            pass
                        else:
                            _table_text['tables'][k1][k2] = v2
        return _table_text

    _output_text = get_ta_text(_output_text)
    _output_text = get_summary_text(_output_text)
    _output_text = get_tables_text(_output_text)
    return _output_text

class OpenPDF(View):
    """[summary]

    Args:
        View ([type]): [description]
    """
    def get(self, request, *args, **kwargs):
        """[summary]

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        def render_to_pdf(template_src, context_dict={}):
            """[summary]

            Args:
                template_src ([type]): [description]
                context_dict (dict, optional): [description]. Defaults to {}.

            Returns:
                [type]: [description]
            """
            template = get_template(template_src)
            html  = template.render(context_dict)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            return None

        _data_dict = {}
        _data_dict.update(self.request.session)
        _data_dict = get_coverage(_data_dict)
        _data_dict = get_output_text(_data_dict)
        pdf = render_to_pdf('pdf.html', _data_dict)
        return HttpResponse(pdf, content_type='application/pdf')


class CodeAutocomplete(autocomplete.Select2QuerySetView):
    """[summary]

    Args:
        autocomplete ([type]): [description]
    """
    def get_queryset(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        forward_type = self.forwarded.get('type', None)
        qs = Code.objects.none()
        if forward_type:
            value = CommodityType.objects.filter(id=forward_type).values_list('commodity_type_en').get()[0]

            qs = Code.objects.filter(type=value).all()
            if self.q:
                qs = Code.objects.filter(type=value).filter(code__icontains=self.q)
        return qs
    
class EntitiesAutocomplete(autocomplete.Select2QuerySetView):
    """[summary]

    Args:
        autocomplete ([type]): [description]
    """
    def get_queryset(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        qs = Organization.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class TypeAutocomplete(autocomplete.Select2QuerySetView):
    """[summary]

    Args:
        autocomplete ([type]): [description]
    """
    def get_queryset(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        qs = CommodityType.objects.all()

        if self.q:
            qs = qs.filter(commodity_type__icontains=self.q)
        
        return qs

def lt_condition(wizard):
    """[summary]

    Args:
        wizard ([type]): [description]

    Returns:
        [type]: [description]
    """
    lt_list = [f[0] for f in FORMS[:3]]

    data_dict = {}
    try:
        for f in lt_list:
            data_dict.update(wizard.get_cleaned_data_for_step(f))
    except:
        return True
    
    data_dict = get_coverage(data_dict)
    
    if sum(data_dict['bool'].values()) == 0:
        return False
    return True


class TradeForm(NamedUrlCookieWizardView):
    """[summary]

    Args:
        NamedUrlCookieWizardView ([type]): [description]

    Returns:
        [type]: [description]
    """
    form_list = [f[1] for f in FORMS]
    url_name=url_name
    done_step_name=done_step_name

    def get_template_names(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        form = [TEMPLATES[self.steps.current]]
        return form

    def get_form(self, step=None, data=None, files=None):
        """[summary]

        Args:
            step ([type], optional): [description]. Defaults to None.
            data ([type], optional): [description]. Defaults to None.
            files ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        form = super(TradeForm, self).get_form(step, data, files)
        
        if 'limited_tendering' in form.fields:
            lt_list = [f[0] for f in FORMS[:3]]
            data_dict = create_data_dict(self, lt_list)
            
            data_dict = get_coverage(data_dict)

            ta_applies = [k for k,v in data_dict['bool'].items() if v is True]

            query_list = []
            if ta_applies:
                qs = LimitedTenderingReason.objects.all()
                for ta in ta_applies:
                    field_name = ta
                    qs = qs.filter(**{field_name: True}).values_list('name')
                qs = [q[0] for q in qs]
                for q in qs:
                    query_list.append(q)
            form.fields['limited_tendering'].queryset = LimitedTenderingReason.objects.filter(name__in=query_list).only('name')
            
        return form

    def done(self, form_list, form_dict, **kwargs):
        """[summary]

        Args:
            form_list ([type]): [description]
            form_dict ([type]): [description]

        Returns:
            [type]: [description]
        """
        done_list = [f[0] for f in FORMS]
        data_dict = create_data_dict(self, done_list)
        data_dict = get_coverage(data_dict)

       
        def add_session_list(name, model):
            """[summary]

            Args:
                name ([type]): [description]
                model ([type]): [description]
            """
            ex_list = []
            v = data_dict[name]
            for ex in v:
                if ex != 'None':
                    check = model.objects.filter(name=ex).values_list('name').get()[0]
                else:
                    check = 'None'
                ex_list.append(check)
            self.request.session[name] = ex_list

        exception_dict = {
            'exceptions': GeneralException,
            'cfta_exceptions': CftaException,
            'limited_tendering': LimitedTenderingReason
        }
        for k, v in exception_dict.items():
            add_session_list(k, v)

        data_fields = ['entities', 'estimated_value', 'type', 'code']
        for field in data_fields:
            self.request.session[field] = str(data_dict[field])

        data_dict = get_output_text(data_dict)
        return render(self.request, 'done.html', data_dict)
