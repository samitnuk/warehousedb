from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ..views import tool

urlpatterns = [

    url(r'^list/',
        login_required(tool.ToolList.as_view()),
        name='tool_list'),

    url(r'^list_by_dates/',
        tool.list_by_dates,
        name='tool_list_by_dates'),

    url(r'^detail/(?P<pk>\d+)/',
        login_required(tool.ToolDetail.as_view()),
        name='tool_detail'),

    url(r'^create/',
        login_required(tool.ToolCreate.as_view()),
        name='tool_create'),

    url(r'^update/(?P<pk>\d+)/',
        login_required(tool.ToolUpdate.as_view()),
        name='tool_update'),

    url(r'^delete/(?P<pk>\d+)/',
        login_required(tool.ToolDelete.as_view()),
        name='tool_delete'),

    url(r'^toolchange_detail/(?P<pk>\d+)/',
        login_required(tool.ToolChangeDetail.as_view()),
        name='toolchange_detail'),

    url(r'^toolchange_create/(?P<tool_pk>\d+)/',
        login_required(tool.ToolChangeCreate.as_view()),
        name='toolchange_create'),

    url(r'^toolchange_update/(?P<pk>\d+)/',
        login_required(tool.ToolChangeUpdate.as_view()),
        name='toolchange_update'),

    url(r'^toolchange_delete/(?P<pk>\d+)/',
        login_required(tool.ToolChangeDelete.as_view()),
        name='toolchange_delete'),
]
