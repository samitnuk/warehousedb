from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ..views import order


urlpatterns = [

    url(r'^list/(?P<status>[\w]+)?/?',
        login_required(order.OrderList.as_view()),
        name='order_list'),

    url(r'^create/',
        login_required(order.OrderCreate.as_view()),
        name='order_create'),

    url(r'^delete/(?P<pk>\d+)/',
        login_required(order.OrderDelete.as_view()),
        name='order_delete'),

    url(r'^detail/(?P<pk>\d+)/',
        login_required(order.OrderDetail.as_view()),
        name='order_detail'),

    url(r'^ready_confirmation/(?P<pk>\d+)/',
        order.ready_confirmation,
        name='order_ready_confirmation'),

    url(r'^sent_confirmation/(?P<pk>\d+)/',
        login_required(order.AddSentNotesToOrder.as_view()),
        name='order_sent_confirmation'),

    url(r'^paid_confirmation/(?P<pk>\d+)/',
        order.paid_confirmation,
        name='order_paid_confirmation'),
]
