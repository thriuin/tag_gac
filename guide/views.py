from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView

from api.serializers import CodeListSerializer
from api.models import CodeList


def Guide(request):
	return render(request, "wine.html", {})


class GuideListing(ListAPIView):
    # set the erializer class
    serializer_class = CodeListSerializer

    def get_queryset(self):
        # filter the queryset based on the filters applied
        queryList = CodeList.objects.all()
        type = self.request.query_params.get('type_en', None)
        code_system = self.request.query_params.get('code_system_en', None)
        code_list = self.request.query_params.get('code_list_en', None)

        if type:
            queryList = queryList.filter(type_en = type)
        if code_system:
            queryList = queryList.filter(code_system_en = code_system)
        if code_list:
            queryList = queryList.filter(code_list_en = code_list)
        return queryList


def getType(request):
    # get all the countreis from the database excluding
    # null and blank values
    if request.method == "GET" and request.is_ajax():
        type = CodeList.objects.exclude(type_en__isnull=True).exclude(type_en__exact='').\
            order_by('type_en').values_list('type_en').distinct()
        type = [i[0] for i in list(type)]
        data = {
            "type_en": type,
        }
        return JsonResponse(data, status = 200)


def getCodeSystem(request):
    if request.method == "GET" and request.is_ajax():
        type = request.GET.get('type_en')
        code_system = CodeList.objects.filter(type_en = type).\
            exclude(code_system_en__null=True).exclude(code_system_en__exact='').\
            order_by('code_system_en').values_list('code_system_en').distinct()
        code_system = [i[0] for i in list(code_system)]
        data = {
            "code_system_en": code_system
        }
        return JsonResponse(data, status=200)



def getCodeList(request):
    # get the provinces for given country from the
    # database excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        code_system = request.GET.get('code_system_en')
        code_list = CodeList.objects.filter(code_system_en=code_system).\
            	exclude(code_list_en__isnull=True).exclude(code_list_en__exact='').\
            	order_by('code_list_en').values_list('code_list_en').distinct()
        code_list = [i[0] for i in list(code_list)]
        data = {
            "code_list_en": code_list,
        }
        return JsonResponse(data, status = 200)
