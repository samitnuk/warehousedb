from django.conf.urls import url

from ..views import products


urlpatterns = [

    url(r'^list/', products.product_list, name='product_list'),

    url(r'^detail/(?P<pk>\d+)/',
        products.product_detail,
        name='product_detail'),

    url(r'^create/',
        products.product_create,
        name='product_create'),

    url(r'^delete/(?P<pk>\d+)/',
        products.product_delete,
        name='product_delete'),

    url(r'^create_std_cable/',
        products.product_create_std_cable,
        name='product_create_std_cable'),

    url(r'^create_tza_cable/',
        products.product_create_tza_cable,
        name='product_create_tza_cable'),

    url(r'^create_b_cable/',
        products.product_create_b_cable,
        name='product_create_b_cable'),

    url(r'^create_h_cable/',
        products.product_create_h_cable,
        name='product_create_h_cable'),
]
