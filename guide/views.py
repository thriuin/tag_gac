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
		code_system = self.request.query_params.get('code_system_en', None)
		code_list = self.request.query_params.get('code_list_en', None)

		if code_system:
		    queryList = queryList.filter(code_system_en = code_system)
		if code_list:
		    queryList = queryList.filter(code_list_en = code_list)
		return queryList



def getCodeSystem(request):
    # get all the countreis from the database excluding
    # null and blank values
    if request.method == "GET" and request.is_ajax():
        code_system = CodeList.objects.exclude(code_system_en__isnull=True).\
            exclude(code_list_en__exact='').order_by('code_system_en').values_list('code_system_en').distinct()
        code_system = [i[0] for i in list(code_system)]
        data = {
            "code_system_en": code_system,
        }
        print(data)
        return JsonResponse(data, status = 200)



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
