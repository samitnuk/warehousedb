from django.conf.urls import url

from ..views import item


urlpatterns = [

    url(r'^$', item.list_, name='item_list'),

    url(r'^item/list_by_dates/',
        item.list_by_dates,
        name='item_list_by_dates'),

    url(r'^item/list_by_categories/(?P<category_pk>\d+)?/?',
        item.list_by_categories,
        name='item_list_by_categories'),

    url(r'^item/detail/(?P<pk>\d+)/',
        item.detail,
        name='item_detail'),

    url(r'^item/create/',
        item.create,
        name='item_create'),

    url(r'^item/itemchange_detail/(?P<pk>\d+)/',
        item.itemchange_detail,
        name='itemchange_detail'),

    url(r'^item/itemchange_create/(?P<pk>\d+)/',
        item.itemchange_create,
        name='itemchange_create'),
]
