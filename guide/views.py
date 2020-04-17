from django.shortcuts import render
from guide.models import Code, Instructions, ValueThreshold, Entities, TAException, TenderingReason, CftaException
from guide.forms import MandatoryElementsEN, ExceptionsEN, LimitedTenderingEN, CftaExceptionsEN
from formtools.wizard.views import NamedUrlSessionWizardView
from django.http import JsonResponse

FORMS = [("0", MandatoryElementsEN),
         ("1", ExceptionsEN),
         ("2", LimitedTenderingEN),
         ("3", CftaExceptionsEN)]

TEMPLATES = {"0": "mandatory_elements.html",
             "1": "exceptions.html",
             "2": "limited_tendering.html",
             "3": "cfta_exceptions.html"}


class TradeForm(NamedUrlSessionWizardView):
    form_list = [MandatoryElementsEN, ExceptionsEN, LimitedTenderingEN, CftaExceptionsEN]
    url_name = 'guide:form_step'
    done_step_name = 'guide:done_step'

    def get_template_names(self):
        form = [TEMPLATES[self.steps.current]]
        return form

    def done(self, form_list, form_dict, **kwargs):
        trade_agreements = {
            'nafta_annex': {}, 
            'ccfta': {}, 
            'ccofta': {}, 
            'chfta': {}, 
            'cpafta': {}, 
            'cpfta': {}, 
            'ckfta': {}, 
            'cufta': {}, 
            'wto_agp': {}, 
            'ceta': {}, 
            'cptpp': {}, 
            'cfta': {}
            }

        context_dict = {}
        for form in form_list:
            for k, v in form.cleaned_data.items():
                context_dict[k] = v
                for k2 in trade_agreements.keys():
                    trade_agreements[k2][k] = True
        context_dict['ta'] = trade_agreements

        def value_threshold_rule(context, col1, col2):
            value = context[col1]
            type = context[col2]
            try:
                for ta in trade_agreements:
                    check = ValueThreshold.objects.filter(type_value=type).values_list(ta).get()[0]
                    if value < check:
                        context['ta'][ta][col1] = False
                    else:
                        context['ta'][ta][col1] = True
            except:
                raise ValueError
            return context
        context_dict = value_threshold_rule(context_dict, 'estimated_value', 'type')

        def entities_rule(context, col):
            entity = context_dict[col]
            try:
                for ta in trade_agreements:
                    check = Entities.objects.filter(name=entity).values_list(ta).get()[0]
                    if check is False:
                        context['ta'][ta][col] = False
                    else:
                        context['ta'][ta][col] = True
            except:
                raise ValueError
            return context
        context_dict = entities_rule(context_dict, 'entities')

        def code_rule(context, code_col, type_col, entities_col):
            value = context[code_col]
            type = context[type_col]
            entity = context[entities_col]

            try:
                if type == 'Goods':
                    defence_rule = Entities.objects.filter(name=entity).values_list('weapons_rule').get()[0]
                    for ta in trade_agreements:
                        if defence_rule is False:
                            context['ta'][ta][code_col] = True
                        else:
                            context['ta'][ta][code_col] = False
                        return context
                elif type == 'Construction':
                    tc_rule = Entities.objects.filter(name=entity).values_list('tc').get()[0]
                    for ta in trade_agreements:
                        if tc_rule is False:
                            context['ta'][ta][code_col] = True
                        else:
                            context['ta'][ta][code_col] = False
                    return context
                else:
                    for ta in trade_agreements:
                        check = Code.objects.filter(code=value).values_list(ta).get()[0]
                        if check is False:
                            context['ta'][ta][code_col] = False
                        else:
                            context['ta'][ta][code_col] = True
            except:
                raise ValueError
            return context
        context_dict = code_rule(context_dict, 'code', 'type', 'entities')

        def exceptions_rule(context, col, model):
            if context[col]:
                value = context[col]
                try:
                    for ta in trade_agreements:
                        for ex in value:
                            check = model.objects.filter(name=ex).values_list(ta).get()[0]

                            if (context['ta'][ta][col] is False):
                                pass
                            elif (context['ta'][ta][col] is True) and (check is False):
                                pass
                            elif (context['ta'][ta][col] is True) and (check is True):
                                context['ta'][ta][col] = False
                except:
                    raise ValueError
            else:
                context[col]= ['None']
            return context
        context_dict = exceptions_rule(context_dict, 'exceptions', TAException)
        context_dict = exceptions_rule(context_dict, 'limited_tendering', TenderingReason)
        context_dict = exceptions_rule(context_dict, 'cfta_exceptions', CftaException)

        context_dict['bool'] = {}
        for ta in trade_agreements:
            context_dict['bool'][ta] = True
            for k, v in context_dict['ta'][ta].items():
                 if v is False:
                     context_dict['bool'][ta] = False
        print(context_dict)
        return render(self.request, 'done.html', context_dict)


def getType(request):
    # get all the types from the database
    # null and blank values
    if request.method == "GET" and request.is_ajax():
        type = Code.objects.\
            exclude(type__isnull=True).\
            exclude(type__exact='').\
            order_by('type').\
            values_list('type').\
            distinct()
        type = [i[0] for i in list(type)]
        data = {
            "type": type,
        }
        return JsonResponse(data, status = 200)


def getCode(request):
    # get the type and code systems and filter to get code
    # database excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        type = request.GET.get('type')
        code = Code.objects.\
            filter(type = type).\
            exclude(code__isnull=True).\
            exclude(code__exact='').\
            values_list('code').\
            distinct()
        code = [i[0] for i in list(code)]
        data = {
            "code": code,
        }
        return JsonResponse(data, status = 200)

