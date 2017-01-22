from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ..views import material


urlpatterns = [

    url(r'^list/',
        login_required(material.MaterialList.as_view()),
        name='material_list'),

    url(r'^list_by_dates/',
        material.list_by_dates,
        name='material_list_by_dates'),

    url(r'^detail/(?P<pk>\d+)/',
        login_required(material.MaterialDetail.as_view()),
        name='material_detail'),

    url(r'^create/',
        login_required(material.MaterialCreate.as_view()),
        name='material_create'),

    url(r'^update/(?P<pk>\d+)/',
        login_required(material.MaterialUpdate.as_view()),
        name='material_update'),

    url(r'^delete/(?P<pk>\d+)/',
        login_required(material.MaterialDelete.as_view()),
        name='material_delete'),

    url(r'^materialchange_detail/(?P<pk>\d+)/',
        login_required(material.MaterialChangeDetail.as_view()),
        name='materialchange_detail'),

    url(r'^materialchange_create/(?P<material_pk>\d+)',
        login_required(material.MaterialChangeCreate.as_view()),
        name='materialchange_create'),

    url(r'^materialchange_update/(?P<pk>\d+)/',
        login_required(material.MaterialChangeUpdate.as_view()),
        name='materialchange_update'),

    url(r'^materialchange_delete/(?P<pk>\d+)/',
        login_required(material.MaterialChangeDelete.as_view()),
        name='materialchange_delete'),
]
