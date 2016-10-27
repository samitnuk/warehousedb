from django.conf.urls import url

from ..views import tool


urlpatterns = [

    url(r'^list/', tool.list_, name='tool_list'),

    url(r'^list_by_dates/',
        tool.list_by_dates,
        name='tool_list_by_dates'),

    url(r'^detail/(?P<pk>\d+)/',
        tool.detail,
        name='tool_detail'),

    url(r'^create/',
        tool.create,
        name='tool_create'),

    url(r'^delete/(?P<pk>\d+)/',
        tool.delete,
        name='tool_delete'),

    url(r'^toolchange_detail/(?P<pk>\d+)/',
        tool.toolchange_detail,
        name='toolchange_detail'),

    url(r'^toolchange_create/(?P<pk>\d+)/',
        tool.toolchange_create,
        name='toolchange_create'),

    url(r'^toolchange_delete/(?P<pk>\d+)/',
        tool.toolchange_delete,
        name='toolchange_delete'),
]
