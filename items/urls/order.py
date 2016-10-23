from django.conf.urls import url

from ..views import order


urlpatterns = [

    url(r'^list/', order.list_, name='order_list'),

    url(r'^create/',
        order.create,
        name='order_create'),

    url(r'^delete/(?P<pk>\d+)/',
        order.delete,
        name='order_delete'),
]
