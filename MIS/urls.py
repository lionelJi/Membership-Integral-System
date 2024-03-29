"""MIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from MIS import views

import xadmin
from xadmin.plugins import xversion

xadmin.autodiscover()

xversion.register_models()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # xadmin的配置
    url(r'xadmin', include(xadmin.site.urls)),
    url(r'^$', views.index, name='index'),
    # 商品部分
    url(r'^mall/', include('mall.urls', namespace='mall')),
    # 个人中心
    url(r'^mine/', include('mine.urls', namespace='mine')),
    # 系统模块
    url(r'^sys/', include('system.urls', namespace='system')),
    # 账户模块
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
