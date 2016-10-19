from django.conf.urls import url

from . import views

urlpatterns = [

    # items, itemchanges & categories
    # -----------------------------------------------------------------
    url(r'^$', views.main, name='main'),    # item_list

    url(r'^item_list_by_dates/', views.item_list_by_dates,
        name='item_list_by_dates'),

    url(r'^item_list_by_categories/(?P<pk>\d+)?/?',
        views.item_list_by_categories,
        name='item_list_by_categories'),

    url(r'^item_details/(?P<pk>\d+)/', views.item_detail,
        name='item_detail'),

    url(r'^itemchange_detail/(?P<pk>\d+)/', views.itemchange_detail,
        name='itemchange_detail'),

    url(r'^itemchange_create/(?P<pk>\d+)/', views.itemchange_create,
        name='itemchange_create'),

    # products
    # -----------------------------------------------------------------
    url(r'^product_create/', views.product_create,
        name='product_create'),

    url(r'^product_list/', views.product_list,
        name='product_list'),

    url(r'^product_detail/(?P<pk>\d+)/', views.product_detail,
        name='product_detail'),

    url(r'^product_create_std_cable/', views.product_create_std_cable,
        name='product_create_std_cable'),

    url(r'^product_create_tza_cable/', views.product_create_tza_cable,
        name='product_create_tza_cable'),

    url(r'^product_create_B_cable/', views.product_create_B_cable,
        name='product_create_B_cable'),

    # orders
    # -----------------------------------------------------------------
    url(r'^order_list/', views.order_list,
        name='order_list'),

    url(r'^order_create/', views.order_create,
        name='order_create'),

    # url(r'^order_delete/', views.order_delete,
    #     name='order_delete'),

    # materials & materialchanges
    # -----------------------------------------------------------------
    # rl(r'^material_list/', views.material_list,
    #     name='material_list'),

    # url(r'^material_create/', views.material_create,
    #     name='material_create'),

    # url(r'^material_delete/', views.material_delete,
    #     name='material_delete'),

    # url(r'^material_detail/', views.material_detail,
    #     name='material_detail'),

    # url(r'^material_list_by_dates/', views.material_list_by_dates,
    #     name='material_list_by_dates'),

    # url(r'^materialchange_detail/(?P<pk>\d+)/', views.materialchange_detail,
    #     name='materialchange_detail'),

    # url(r'^materialchange_create/(?P<pk>\d+)/', views.materialchange_create,
    #     name='materialchange_create'),

    # tools & toolchanges
    # -----------------------------------------------------------------
    # rl(r'^tool_list/', views.tool_list,
    #     name='tool_list'),

    # url(r'^tool_create/', views.tool_create,
    #     name='tool_create'),

    # url(r'^tool_delete/', views.tool_delete,
    #     name='tool_delete'),

    # url(r'^tool_detail/', views.tool_detail,
    #     name='tool_detail'),

    # url(r'^tool_list_by_dates/', views.tool_list_by_dates,
    #     name='tool_list_by_dates'),

    # url(r'^toolchange_detail/(?P<pk>\d+)/', views.toolchange_detail,
    #     name='toolchange_detail'),

    # url(r'^toolchange_create/(?P<pk>\d+)/', views.toolchange_create,
    #     name='toolchange_create'),

    # login & logout
    # -----------------------------------------------------------------
    url(r'^login/', views.login, name='login'),

    url(r'^logout/', views.logout, name='logout'),
]
