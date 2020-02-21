from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns=[
    path('', RedirectView.as_view(pattern_name='info_list_view'), name='home'),
    path('guide/', include('guide.urls'))
]

