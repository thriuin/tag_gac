from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from guide.views import GuideFormView, getType, getCodeSystem, getCode



urlpatterns = [
    path('', GuideFormView.as_view()),
    path('evaluate/', GuideFormView.as_view(), name='Evaluate Form'),
    path("ajax/type/", getType, name = 'get_type'),
    path("ajax/code_system/", getCodeSystem, name = 'get_code_system'),
	path("ajax/code/", getCode, name = 'get_code')
]