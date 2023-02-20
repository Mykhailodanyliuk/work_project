from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.uspto_page, name='uspto'),
    path('<pk>', views.uspto_patent_data, name='uspto_patent_data'),
]