from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.hhs_page, name='nppes_data'),
    path('data/<npi_id>/', views.hhs_data_page, name='hhs_data'),
    path('individual/', views.display_hhs_data_individual, name='individual_npis'),
    path('entities/', views.display_hhs_data_entities, name='entities_npis'),
    path('search', views.hhs_data_search, name='nppes_data_search'),
]