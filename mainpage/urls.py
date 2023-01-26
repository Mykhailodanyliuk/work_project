from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('npi_data', views.get_list_npi_data, name='npi_companies_page'),
    path('npi_data_search', views.npi_data_search, name='npi_data_search'),
]




