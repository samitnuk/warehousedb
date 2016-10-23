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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from items.views import login, logout

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^item/', include('items.urls.item')),
    url(r'^product/', include('items.urls.product')),
    url(r'^order/', include('items.urls.order')),
    url(r'^material/', include('items.urls.material')),
    url(r'^tool/', include('items.urls.tool')),

    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
