from django.conf.urls import url

from ..views import orders


urlpatterns = [

    url(r'^list/', orders.order_list, name='order_list'),

    url(r'^create/',
        orders.order_create,
        name='order_create'),

    url(r'^delete/(?P<pk>\d+)/',
        orders.order_delete,
        name='order_delete'),
]
