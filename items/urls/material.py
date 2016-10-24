from django.conf.urls import url

from ..views import material


urlpatterns = [

    url(r'^list/', material.list_, name='material_list'),

    url(r'^list_by_dates/',
        material.list_by_dates,
        name='material_list_by_dates'),

    url(r'^detail/(?P<pk>\d+)/',
        material.detail,
        name='material_detail'),

    url(r'^create/',
        material.create,
        name='material_create'),

    url(r'^delete/(?P<pk>\d+)/',
        material.delete,
        name='material_delete'),

    url(r'^materialchange_detail/(?P<pk>\d+)/',
        material.materialchange_detail,
        name='materialchange_detail'),

    url(r'^materialchange_create/',
        material.materialchange_create,
        name='materialchange_create'),

    url(r'^materialchange_delete/(?P<pk>\d+)/',
        material.materialchange_delete,
        name='materialchange_delete'),
]