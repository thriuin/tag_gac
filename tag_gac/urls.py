"""tag_gac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from guide.views import GuideView, GoodsOGDViewSet, ConstructionViewSet, ServicesViewSet, \
    TenderingReasonsViewSet, GuideFormView


urlpatterns = [
    path('tag/admin/', admin.site.urls),
    path('tag/', GuideFormView.as_view(), name='Guide'),
    path('tag/guide/', GuideView.as_view(), name='Guide'),  # Temporary demo of SurveyJS
    path('tag/goods/', GoodsOGDViewSet.as_view({'get': 'list'})),
    path('tag/construction/', ConstructionViewSet.as_view({'get': 'list'})),
    path('tag/services/', ServicesViewSet.as_view({'get': 'list'})),
    path('tag/tendering_reasons/', TenderingReasonsViewSet.as_view({'get': 'list'})),
    path('tag/evaluate/', GuideFormView.as_view(), name='EvaluateForm')
]
