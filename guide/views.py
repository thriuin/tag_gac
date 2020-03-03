from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from api.serializers import CodeSerializer
from api.models import Code
from guide.forms import GuideForm


def CodeView(request):
    if request.method == "POST":
        form = GuideForm()
    else:
        form = GuideForm()
    return render(request, "guide.html", {'form': form})


class CodeListView(ListAPIView):
    serializer_class = CodeSerializer

    def get_queryset(self):
        # filter the queryset based on the filters applied
        queryList = Code.objects.all()
        type = self.request.query_params.get('type_en', None)
        code_system = self.request.query_params.get('code_system_en', None)
        code = self.request.query_params.get('code_en', None)

        if type:
            queryList = queryList.filter(type_en = type)
        if code_system:
            queryList = queryList.filter(code_system_en = code_system)
        if code:
            queryList = queryList.filter(code_en = code)


def getType(request):
    # get all the types from the database
    # null and blank values
    if request.method == "GET" and request.is_ajax():
        type = Code.objects.\
            exclude(type_en__isnull=True).\
            exclude(type_en__exact='').\
            order_by('type_en').\
            values_list('type_en').\
            distinct()
        type = [i[0] for i in list(type)]
        data = {
            "type_en": type,
        }
        return JsonResponse(data, status = 200)


def getCodeSystem(request):
    # get the code systems from the database
    # database excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        type = request.GET.get('type_en')
        code_system = Code.objects.\
            filter(type_en = type).\
            exclude(code_system_en__isnull=True).\
            exclude(code_system_en__exact='').\
            order_by('code_system_en').\
            values_list('code_system_en').\
            distinct()
        code_system = [i[0] for i in list(code_system)]
        data = {
            "code_system_en": code_system,
        }
        return JsonResponse(data, status = 200)


def getCode(request):
    # get the type and code systems and filter to get code
    # database excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        code_system = request.GET.get('code_system_en')
        type = request.GET.get('type_en')
        code = Code.objects.\
            filter(type_en = type).\
            filter(code_system_en = code_system).\
            exclude(code_en__isnull=True).\
            exclude(code_en__exact='').\
            values_list('code_en').\
            distinct()
        code = [i[0] for i in list(code)]
        data = {
            "code_en": code,
        }
        return JsonResponse(data, status = 200)
