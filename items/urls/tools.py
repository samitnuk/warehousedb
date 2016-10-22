from django.conf.urls import url

from ..views import tools


urlpatterns = [

    url(r'^list/', tools.tool_list, name='tool_list'),

    url(r'^list_by_dates/',
        tools.tool_list_by_dates,
        name='tool_list_by_dates'),

    url(r'^detail/(?P<pk>\d+)/',
        tools.tool_detail,
        name='tool_detail'),

    url(r'^create/',
        tools.tool_create,
        name='tool_create'),

    url(r'^delete/(?P<pk>\d+)/',
        tools.tool_delete,
        name='tool_delete'),

    url(r'^toolchange_detail/(?P<pk>\d+)/',
        tools.toolchange_detail,
        name='toolchange_detail'),

    url(r'^toolchange_create/',
        tools.toolchange_create,
        name='toolchange_create'),

    url(r'^toolchange_delete/(?P<pk>\d+)/',
        tools.toolchange_delete,
        name='toolchange_delete'),
]
