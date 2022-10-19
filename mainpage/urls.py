from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('sec_company_tickers', views.sec_company_tickers, name='sec_company_tickers'),
    path('sec_company_fillings', views.sec_company_fillings, name='sec_company_fillings'),
    path('npi_data', views.get_list_npi_data, name='mpi_companies_page'),
    path('companies_data/<cik>/', views.get_company_data, name='get_company_data'),
    path('nppes_data', views.nppes_data_page, name='nppes_data'),
    path('nppes_data/<npi>/', views.nppes_data, name='nppes_data'),
    path('medical_trials', views.medical_trials, name='medical_trials'),
    path('medical_trials/<org_id>/', views.display_organization_trials, name='nppes_data'),
    path('trials/<trial_id>/', views.display_clinical_trial, name='trials'),
]




