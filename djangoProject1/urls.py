"""
URL configuration for djangoProject1 project.

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
from django.urls import path,include
from djangoProject1 import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('login/', views.login, name='login'),
    path('account/',views.account,name='account'),
    path('auth/',views.auth, name='auth'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password2/', views.change_password2, name='change_password2'),
    path('change_email1/', views.change_email1, name='change_email1'),
    path('change_email2/', views.change_email2, name='change_email2'),
    path('change_email3/', views.change_email3, name='change_email3'),



]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)