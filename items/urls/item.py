from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

from ..views import item

urlpatterns = [

    url(r'^$',
        RedirectView.as_view(pattern_name='item_list', permanent=False)),

    url(r'^item/list/(?P<category_pk>\d+)?/?',
        login_required(item.ItemList.as_view()),
        name='item_list'),

    url(r'^item/list_print/',
        login_required(item.ItemListPrint.as_view()),
        name='item_list_print'),

    url(r'^item/list_by_dates/',
        item.list_by_dates,
        name='item_list_by_dates'),

    url(r'^item/detail/(?P<pk>\d+)/',
        login_required(item.ItemDetail.as_view()),
        name='item_detail'),

    url(r'^item/create/',
        login_required(item.ItemCreate.as_view()),
        name='item_create'),

    url(r'^item/update/(?P<pk>\d+)/',
        login_required(item.ItemUpdate.as_view()),
        name='item_update'),

    url(r'^item/delete/(?P<pk>\d+)/',
        login_required(item.ItemDelete.as_view()),
        name='item_delete'),

    url(r'^item/itemchange_detail/(?P<pk>\d+)/',
        login_required(item.ItemChangeDetail.as_view()),
        name='itemchange_detail'),

    url(r'^item/itemchange_create/(?P<item_pk>\d+)/',
        login_required(item.ItemChangeCreate.as_view()),
        name='itemchange_create'),

    url(r'^item/itemchange_update/(?P<pk>\d+)/',
        login_required(item.ItemChangeUpdate.as_view()),
        name='itemchange_update'),

    url(r'^item/itemchange_delete/(?P<pk>\d+)/',
        login_required(item.ItemChangeDelete.as_view()),
        name='itemchange_delete'),
]
