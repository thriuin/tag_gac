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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView

admin.site.site_header = "TAG Admin"
admin.site.site_title = "TAG Admin Portal"
admin.site.index_title = "TAG Admin Portal"

urlpatterns = [
    path('tag/admin/doc/', include('django.contrib.admindocs.urls')),
    path('tag/admin/', admin.site.urls),
    path(r"tag/", include(('guide.urls', 'guide'), namespace = 'guide')),
    re_path('', RedirectView.as_view(url='tag/form/0/')),
    re_path(r'^.*$', RedirectView.as_view(url='tag/form/0/'))
]
