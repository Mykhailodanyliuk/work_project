"""medical_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404 , handler500

from medical_site import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainpage.urls')),
    path('clinical_trials/', include('clinical_trials.urls')),
    path('sec/', include('sec.urls')),
    path('hhs/', include('hhs.urls')),
    path('fda/', include('fda.urls')),
    path('uspto/', include('uspto.urls')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'mainpage.views.error_404'
handler500 = 'mainpage.views.error_500'