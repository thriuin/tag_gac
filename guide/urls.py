from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from guide.views import CodeViewEN, CodeViewFR, getType, getCode


urlpatterns = [
    path('en/', CodeViewEN.as_view()),
    path('fr/', CodeViewFR.as_view()),
    path('en/evaluate/', CodeViewEN.as_view(), name='Evaluate Form'),
    path("ajax/type/", getType, name = 'get_type'),
	path("ajax/code/", getCode, name = 'get_code')
]