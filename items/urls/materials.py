from django.conf.urls import url

from ..views import materials


urlpatterns = [

    url(r'^list/', materials.material_list, name='material_list'),

    url(r'^list_by_dates/',
        materials.material_list_by_dates,
        name='material_list_by_dates'),

    url(r'^detail/(?P<pk>\d+)/',
        materials.material_detail,
        name='material_detail'),

    url(r'^create/',
        materials.material_create,
        name='material_create'),

    url(r'^delete/(?P<pk>\d+)/',
        materials.material_delete,
        name='material_delete'),

    url(r'^materialchange_detail/(?P<pk>\d+)/',
        materials.materialchange_detail,
        name='materialchange_detail'),

    url(r'^materialchange_create/',
        materials.materialchange_create,
        name='materialchange_create'),

    url(r'^materialchange_delete/(?P<pk>\d+)/',
        materials.materialchange_delete,
        name='materialchange_delete'),
]
