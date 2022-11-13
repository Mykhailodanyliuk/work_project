from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('sec_company_tickers', views.sec_company_tickers, name='sec_company_tickers'),
    path('sec_company_fillings', views.sec_company_fillings, name='sec_company_fillings'),
    path('companies_data/<cik>/', views.get_company_data, name='get_company_data'),
    path('npi_data', views.get_list_npi_data, name='mpi_companies_page'),
    path('nppes_data', views.nppes_data_page, name='nppes_data'),
    path('nppes_data/individual/<npi_id>/', views.nppes_data, name='individual_npi'),
    path('nppes_data/entities/<npi_id>/', views.nppes_data, name='entities_npi'),
    path('nppes_data/individual/', views.display_nppes_data_individual, name='individual_npis'),
    path('nppes_data/entities/', views.display_nppes_data_entities, name='entities_npis'),
    path('clinical_trials', views.medical_trials, name='clinical_trials'),
    path('clinical_trials/<org_id>/', views.display_organization_trials, name='clinical_trial'),
    path('clinical_trial/<trial_id>/', views.display_clinical_trial, name='trials'),
    path('my_search', views.my_search, name='my_search'),
    path('sec_company_tickers_search', views.sec_company_tickers_search, name='sec_company_tickers_search'),
    path('sec_company_fillings_search', views.sec_company_fillings_search, name='sec_company_fillings_search'),
    path('npi_data_search', views.npi_data_search, name='npi_data_search'),
    path('nppes_data_search', views.nppes_data_search, name='nppes_data_search'),
]




