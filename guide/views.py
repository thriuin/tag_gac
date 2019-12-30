from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
from guide.forms import GuideForm
from guide.models import GoodsCodes, ConstructionCodes, ServicesCodes, TenderingReasons
from guide.serializers import GoodsSerializer, ConstructionSerializer, ServicesSerializer, TenderingSerializer


class GoodsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Goods Procurement Codes to be viewed or edited.
    """
    queryset = GoodsCodes.objects.all().order_by('fs_code_desc')
    serializer_class = GoodsSerializer


class ConstructionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Construction Procurement Codes  to be viewed or edited.
    """
    queryset = ConstructionCodes.objects.all().order_by('fs_code_desc')
    serializer_class = ConstructionSerializer


class ServicesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Services Procurement Codes  to be viewed or edited.
    """
    queryset = ServicesCodes.objects.all().order_by('ccs_level_2')
    serializer_class = ServicesSerializer


class TenderingReasonsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tendering Reasons to be viewed or edited.
    """
    queryset = TenderingReasons.objects.all().order_by('desc_en')
    serializer_class = TenderingSerializer


class GuideView(View):

    def __init__(self):
        super().__init__()

    def get(self, request):
        context = dict()
        
        return render(request, "guide.html", context)


def find_exemptions(form):
    agreements = {
        'nafta_annex': False,
        'ccfta': False,
        'ccofta': False,
        'chfta': False,
        'cpafta': False,
        'cpfta': False,
        'ckfta': False,
        'cufta': False,
        'wto_agp': False,
        'ceta': False,
        'cptpp': False,
    }
    dollars = form.cleaned_data['estimated_value']
    if 'goods_codes' in form.cleaned_data and form.cleaned_data['goods_codes'] is not None:
        goods = GoodsCodes.objects.get(id=form.cleaned_data['goods_codes'].id)
    else:
        goods = None
    if 'services_code' in form.cleaned_data and form.cleaned_data['services_codes'] is not None:
        services = ServicesCodes.objects.get(id=form.cleaned_data['services_codes'].id)
    else:
        services = None
    if 'construction_codes' in form.cleaned_data and form.cleaned_data['construction_codes'] is not None:
        construction = ConstructionCodes.objects.get(id=form.cleaned_data['construction_codes'].id)
    else:
        construction = None
    if dollars > 10000:
        for ta in agreements:
            ta = True
    return agreements

class GuideFormView(View):
    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        form = GuideForm()
        return render(request, 'guide_form.html', {'form': form, 'show_eval': False})

    def post(self, request, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = GuideForm(request.POST)
        context = {'show_eval': False}
        # check whether it's valid:
        if form.is_valid():
            ta = find_exemptions(form)
            context = ta
            context['show_eval'] = True
            print('Valid')
        context['form'] = form
        return render(request, 'guide_form.html', context)


class EvaluateResults(View):

    def __init__(self):
        super().__init__()

    def get(self, request: HttpRequest):
        if request.method == 'POST':
            post_data = request.POST
            print(post_data)

