from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ..views import item


urlpatterns = [

    url(r'^$',
        login_required(item.ItemList.as_view()),
        name='item_list'),

    url(r'^item/list_by_dates/',
        item.list_by_dates,
        name='item_list_by_dates'),

    url(r'^item/list_by_categories/(?P<category_pk>\d+)?/?',
        item.list_by_categories,
        name='item_list_by_categories'),

    url(r'^item/detail/(?P<pk>\d+)/',
        login_required(item.ItemDetail.as_view()),
        name='item_detail'),

    url(r'^item/create/',
        login_required(item.ItemCreate.as_view()),
        name='item_create'),

    url(r'^item/itemchange_detail/(?P<pk>\d+)/',
        login_required(item.ItemChangeDetail.as_view()),
        name='itemchange_detail'),

    url(r'^item/itemchange_create/(?P<item_pk>\d+)/',
        login_required(item.ItemChangeCreate.as_view()),
        name='itemchange_create'),
]
