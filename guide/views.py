from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
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
