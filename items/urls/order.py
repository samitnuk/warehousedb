from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ..views import order


urlpatterns = [

    url(r'^list/',
        login_required(order.OrderList.as_view()),
        name='order_list'),

    url(r'^create/',
        login_required(order.OrderCreate.as_view()),
        name='order_create'),

    url(r'^delete/(?P<pk>\d+)/',
        login_required(order.OrderDelete.as_view()),
        name='order_delete'),
]
