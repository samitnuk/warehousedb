from django.conf.urls import url

from ..views import item


urlpatterns = [

    url(r'^list/', item.list_, name='item_list'),

    url(r'^list_by_dates/',
        item.list_by_dates,
        name='item_list_by_dates'),

    url(r'^list_by_categories/(?P<pk>\d+)?/?',  # category <pk>
        item.list_by_categories,
        name='item_list_by_categories'),

    url(r'^detail/(?P<pk>\d+)/',
        item.detail,
        name='item_detail'),

    url(r'^create/',
        item.create,
        name='item_create'),

    url(r'^itemchange_detail/(?P<pk>\d+)/',
        item.itemchange_detail,
        name='itemchange_detail'),

    url(r'^itemchange_create/(?P<pk>\d+)/',
        item.itemchange_create,
        name='itemchange_create'),
]
