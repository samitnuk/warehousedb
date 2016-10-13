from django.conf.urls import url

from . import views

urlpatterns = [

    # items & categories
    url(r'^$',
        views.main,
        name='main'),

    url(r'^item_list_by_dates/',
        views.item_list_by_dates,
        name='item_list_by_dates'),

    url(r'^item_list_by_categories/(?P<pk>\d+)?/?',
        views.item_list_by_categories,
        name='item_list_by_categories'),

    url(r'^item_details/(?P<pk>\d+)/',
        views.item_detail,
        name='item_detail'),

    url(r'^itemchange_detail/(?P<pk>\d+)/',
        views.itemchange_detail,
        name='itemchange_detail'),

    url(r'^itemchange_create/(?P<pk>\d+)/',
        views.itemchange_create,
        name='itemchange_create'),

    # products
    url(r'^product_create/',
        views.product_create,
        name='product_create'),

    url(r'^product_list/',
        views.product_list,
        name='product_list'),

    url(r'^product_detail/(?P<pk>\d+)/',
        views.product_detail,
        name='product_detail'),

    url(r'^product_create_std_cable/',
        views.product_create_std_cable,
        name='product_create_std_cable'),

    url(r'^product_create_tza_cable/',
        views.product_create_tza_cable,
        name='product_create_tza_cable'),

    url(r'^product_create_B_cable/',
        views.product_create_B_cable,
        name='product_create_B_cable'),

    # orders
    url(r'^order_list/',
        views.order_list,
        name='order_list'),

    url(r'^order_create/',
        views.order_create,
        name='order_create'),

    # login & logout
    url(r'^login/',
        views.login,
        name='login'),

    url(r'^logout/',
        views.logout,
        name='logout'),
]
