"""
URL configuration for reportbump project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from report_potholes.views import PotholeCreateView, ApprovedPotholeMapView, PotholeDetailView, PotholeThanksView

app_name = 'reportbump'

urlpatterns = [
    # libre photoles
    path('', views.index, name='index'),
    # path('report/', PotholeCreateView.as_view(), name='report'),
    # path('thanks/', PotholeThanksView.as_view(), name='thanks'),
    path('maps/', ApprovedPotholeMapView.as_view(), name='maps'),
    path('detail/<int:pk>/', PotholeDetailView.as_view(), name='pothole_detail'),

    #fin libre photoles
    
    path('admin-django/', admin.site.urls),
    path('admin/', include('admin_ssu.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)