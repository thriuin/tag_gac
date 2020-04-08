from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from guide.models import Code, Instructions, ValueThreshold, Entities, TAException, TenderingReason, CftaException
from guide.forms import MandatoryElementsEN, ExceptionsEN, LimitedTenderingEN, CftaExceptionsEN
from django.views.generic import View
from formtools.wizard.views import NamedUrlSessionWizardView
from collections import OrderedDict


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

    def render_revalidation_failure(self, failed_step, form, **kwargs):
            """
            When a step fails, we have to redirect the user to the first failing
            step.
            """
            
            self.storage.current_step = failed_step
            print('failed_step')
            print(failed_step)
            if failed_step == '0':
                print('the failed step is zero')
            return redirect(self.get_step_url(failed_step))

    def render_done(self, form, **kwargs):
        """
        This method gets called when all forms passed. The method should also
        re-validate all steps to prevent manipulation. If any form fails to
        validate, `render_revalidation_failure` should get called.
        If everything is fine call `done`.
        """
        final_forms = OrderedDict()
        # walk through the form list and try to validate the data again.
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            final_forms[form_key] = form_obj

        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(final_forms.values(), form_dict=final_forms, **kwargs)
        self.storage.reset()
        return done_response

    def get_template_names(self):
        form = [TEMPLATES[self.steps.current]]
        return form

    def post(self, *args, **kwargs):
        """
        This method handles POST requests.
        The wizard will render either the current step (if form validation
        wasn't successful), the next step (if the current step was stored
        successful) or the done view (if no more steps are available)
        """
        # Look for a wizard_goto_step element in the posted data which
        # contains a valid step name. If one was found, render the requested
        # form. (This makes stepping back a lot easier).
        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)
        if wizard_goto_step and wizard_goto_step in self.get_form_list():
            return self.render_goto_step(wizard_goto_step)


        # get the form for the current step
        form = self.get_form(data=self.request.POST, files=self.request.FILES)
        print('does it get here')
        # and try to validate
        if form.is_valid():
            # if the form is valid, store the cleaned data and files.
            self.storage.set_step_data(self.steps.current, self.process_step(form))
            self.storage.set_step_files(self.steps.current, self.process_step_files(form))

            # check if the current step is the last step
            if self.steps.current == self.steps.last:
                # no more steps, render done view
                return self.render_done(form, **kwargs)
            else:
                # proceed to the next step
                return self.render_next_step(form)
        print('form not valid')
        return self.render(form)

    def done(self, form_list, **kwargs):
        print('done')
        form_data = process_form_data(form_list)
        print(form_data)
        return render(self.request, 'done.html', {
            'form_data': form_data
        })

def process_form_data(form_list):
    return form_list

    
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

