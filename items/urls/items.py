from django.conf.urls import url

from ..views import items


urlpatterns = [

    url(r'^list/', items.item_list, name='item_list'),

    url(r'^list_by_dates/',
        items.item_list_by_dates,
        name='item_list_by_dates'),

    url(r'^list_by_categories/(?P<pk>\d+)?/?',  # category <pk>
        items.item_list_by_categories,
        name='item_list_by_categories'),

    url(r'^detail/(?P<pk>\d+)/',
        items.item_detail,
        name='item_detail'),

    url(r'^create/',
        items.item_create,
        name='item_create'),

    url(r'^itemchange_detail/(?P<pk>\d+)/',
        items.itemchange_detail,
        name='itemchange_detail'),

    url(r'^itemchange_create/(?P<pk>\d+)/',
        items.itemchange_create,
        name='itemchange_create'),
]
