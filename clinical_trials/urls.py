from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_clinical_trials_organizations, name='clinical_trials_organizations'),
    path('organizations/<org_id>', views.display_organization_trials, name='clinical_trials_organization'),
    path('trial/<trial_id>', views.display_clinical_trial, name='clinical_trial'),
    path('search', views.clinical_trials_organization_search, name='clinical_trials_organization_search'),
]
