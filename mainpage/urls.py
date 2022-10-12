from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('companies_data', views.get_list_companies_page, name='list_companies_page'),
    path('npi_data', views.get_list_npi_data, name='mpi_companies_page'),
    path('companies_data/<cik>/', views.get_company_data, name='get_company_data'),
    path('data_management', views.data_management, name='data_management'),
    path('update_data', views.update_data, name='update_data'),
    path('download_data', views.download_data, name='download_data'),
]




