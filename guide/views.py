from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from guide.models import Code, Instructions, ValueThreshold, Entities, TAException, TenderingReason, CftaException
from guide.forms import GuideFormEN, GuideFormFR
from django.views.generic import View

reason = {
    'entities': {},
    'estimated_value': {},
    'type': {},
    'code': {},
    'exceptions': {},
    'limited_tendering': {},
    'cfta_exceptions': {}
}
trade_agreements = ['nafta_annex', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']
def entities_rule(dic, col):
    '''Check if the trade agreements apply to the entity.'''  
    data = dic[col]        
    try:
        for d in trade_agreements:
            check = Entities.objects.filter(name=data).values_list(d).get()[0]
            if check is False:
                dic['ta'][d][col] = check
            else:
                pass
    except:
        raise ValueError
    return dic


def value_threshold_rule(dic, col1, col2):
    data = dic[col1]
    type = dic[col2]
    try:
        for d in trade_agreements:
            check = ValueThreshold.objects.filter(type_value=type).values_list(d).get()[0]
            if data < check:
                dic['ta'][d][col1] = False
            else:
                dic['ta'][d][col1] = True
    except:
        raise ValueError
    return dic

def code_rule(dic, col, entities, type):
    data = dic[col]
    type = dic[type]
    ent = dic[entities]
    try:
        for agreement in trade_agreements:
            if type == 'Goods':
                defence_rule = Entities.objects.filter(name=ent).values_list('weapons_rule').get()[0]
                if defence_rule is False:
                    dic['ta'][agreement]['code'] = True
                    return dic
                else:
                    pass
            elif type == 'Construction':
                tc_rule = Entities.objects.filter(name=ent).values_list('tc').get()[0]
                if tc_rule is True:
                    dic['ta'][agreement]['code'] = False
                    return dic
                else:
                    pass
            check = Code.objects.filter(code=data).values_list(agreement).get()[0]
            if check is False:
                dic['ta'][agreement]['code'] = False
            else:
                dic['ta'][agreement]['code'] = True
    except:
        raise ValueError
    return dic

def exceptions_rule(dic, col, model):
    data = dic[col] 
    if data:
        for agreement in trade_agreements:
            for x in data:
                check = model.objects.filter(name=x).values_list(agreement).get()[0]
                if check is True:
                    dic['ta'][agreement][col] = False
                else:
                    pass
    else:
        data = ['None']
    return dic


class CodeViewEN(View):

    def get(self, request, *args, **kwargs):
        context_dict = {}
        try:
            context_dict = {'instructions': Instructions.objects.get(id=1)}
        except:
            context_dict = {'instructions': 'No Instructions'}
        form = GuideFormEN()
        context_dict['form'] = form
        context_dict['show_eval']  = False
        return render(request, "guide.html", context_dict)

    def post(self, request, *args, **kwargs):
        
        form = GuideFormEN(request.POST)
        context_dict = {}
        context_dict['form'] = form
        try:
            context_dict = {'instructions': Instructions.objects.get(id=1)}
        except:
            context_dict = {'instructions': 'No Instructions'}
        if form.is_valid():           
            rules = {
                'entities': True,
                'estimated_value': True,
                'type': True,
                'code': True,
                'exceptions': True,
                'limited_tendering': True,
                'cfta_exceptions': True
            }


            reason = {
                'entities': {},
                'estimated_value': {},
                'type': {},
                'code': {},
                'exceptions': {},
                'limited_tendering': {},
                'cfta_exceptions': {}
            }
            trade_agreements = ['nafta_annex', 'ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']
            context_dict['ta'] = {}
            for ta in trade_agreements:
                context_dict['ta'][ta] = {}
                for key, value in rules.items():
                    context_dict['ta'][ta][key] = value
            

            for key in reason.keys():
                if form.cleaned_data is not None:
                    context_dict[key] = form.cleaned_data[key]
                else:
                    context_dict[key] = None

            context_dict = entities_rule(context_dict, 'entities')
            context_dict = value_threshold_rule(context_dict, 'estimated_value', 'type')
            context_dict = code_rule(context_dict, 'code', 'entities', 'type')

            context_dict = exceptions_rule(context_dict, 'exceptions', TAException)
            context_dict = exceptions_rule(context_dict, 'limited_tendering', TenderingReason)
            context_dict = exceptions_rule(context_dict, 'cfta_exceptions', CftaException)

            for ta in trade_agreements:
                if all(context_dict['ta'][ta].values()) is False:
                    context_dict['ta'][ta]['applies'] = False
                else:
                    context_dict['ta'][ta]['applies'] = True
                    
            context_dict['show_eval'] = True
            print(context_dict)
            return render (request, "guide.html", context_dict)
        else:
            context_dict['show_eval']  = False
            return render(request, "guide.html", {'context': context_dict})
        form = GuideFormEN()
        context_dict['form'] = form
        return render(request, "guide.html", context_dict)




class CodeViewFR(View):

    def get(self, request, *args, **kwargs):
        try:
            context_dict = {'instructions': Instructions.objects.get(id=1)}
        except:
            context_dict = {'instructions': 'No instructions'}

        if request.method == "POST":
            context_dict['form'] = GuideFormFR()
        else:
            context_dict['form'] = GuideFormFR()
        return render(request, "guide.html", context_dict)


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

