"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from pybo.views import base_views
from django.views.generic.base import TemplateView
from ocr import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/', include('common.urls')),
    # path('common/', views.index),
    path('pybo/', include('pybo.urls')), # pybo/로 시작되는 페이지 요청은 모두 pybp/urls.py 파일에 있는 url매핑을 쓰란 말
    #path('pybo/', base_views.index, name='index'),  # '/' 에 해당되는 path /
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('upload/', views.upload, name='upload'),
    path('save-image/', views.save_detect, name='save_detect'),
    path('detect/', views.detect, name='detect'),
    path('cropimg/', TemplateView.as_view(template_name='cropimg.html'), name='cropimg'),
    path('transmit/', views.transmit, name='transmit')
]
