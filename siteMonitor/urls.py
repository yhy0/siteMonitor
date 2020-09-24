"""siteMonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from script import views

urlpatterns = [
    path('', admin.site.urls),
    path('email_test', views.email_test),
]

# 配置url 当我们访问 settings.MEDIA_URL中的路径时，static会通过document_root去寻找对应的文件
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)