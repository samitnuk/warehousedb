"""warehousedb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from items import views

urlpatterns = [

    url(r'^$', views.main,
        name='main'),
    url(r'^category/(?P<pk>\d+)/', views.category,
        name='category'),
    url(r'^items_by_dates/', views.items_by_dates,
        name='items_by_dates'),
    url(r'^item_details/(?P<pk>\d+)/', views.item_details,
        name='item_details'),
    url(r'^item_change_details/(?P<pk>\d+)/', views.item_change_details,
        name='item_change_details'),

    url(r'^login/', views.login,
        name='login'),
    url(r'^logout/', views.logout,
        name='logout'),

    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
