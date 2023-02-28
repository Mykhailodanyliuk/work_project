from django.urls import path
from . import views

urlpatterns = [
    path('sec_company_tickers', views.sec_company_tickers, name='sec_company_tickers'),
    path('sec_company_fillings', views.sec_company_fillings, name='sec_company_fillings'),
    path('sec_company_tickers_search', views.sec_company_tickers_search, name='sec_company_tickers_search'),
    path('sec_company_fillings_search', views.sec_company_fillings_search, name='sec_company_fillings_search'),
    path('sec_company_fillings/<cik>', views.display_sec_company_data, name='get_company_data'),
    path('sik_codes', views.display_sic_codes, name='sic_codes'),
]