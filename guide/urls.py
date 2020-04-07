from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from guide.views import getType, getCode, TradeForm
from guide.forms import MandatoryElementsEN, ExceptionsEN, LimitedTenderingEN, CftaExceptionsEN

urlpatterns = [
    url('en/', TradeForm.as_view([MandatoryElementsEN, ExceptionsEN])),
    path("ajax/type/", getType, name = 'get_type'),
	path("ajax/code/", getCode, name = 'get_code')
]