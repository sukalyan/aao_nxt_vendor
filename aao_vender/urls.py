from django.urls import path
from . import views

urlpatterns = [
    path('create_vender/', views.create_vender,name='create_vender'),

    path('view_vender/', views.view_vender, name='view_vender'),
    path('view_vender_pagination/<int:page_number>',views.view_vender_pagination, name='view_vender_pagination'),
    path('vender_details/<int:used_id>',views.vender_details, name='vender_details'),
    path('vender_dashboard/',views.vender_dashboard, name='vender_dashboard'),
    path('vender_add_credit/<int:used_id>',views.vender_add_credit, name='vender_add_credit'),
    path('vender_add_plan/<int:used_id>',views.vender_add_plan, name='vender_add_plan'),

    path('vender_add_per_user_price/<int:used_id>',views.vender_add_per_user_price, name='vender_add_per_user_price'),


    path('create_aao_user/', views.create_aao_user,name='create_aao_user'),
    path('create_aao_user_extend_package/', views.create_aao_user_extend_package,name='create_aao_user_extend_package'),



    path('view_aao_user/', views.view_aao_user,name='view_aao_user'),
    path('view_aao_user_pagination/<int:page_number>', views.view_aao_user_pagination,name='view_aao_user_pagination'),
    path('vender_transection_view/', views.vender_transection_view,name='vender_transection_view'),
    path('vender_transection_view_pagination/<int:page_number>', views.vender_transection_view_pagination,name='vender_transection_view_pagination'),
    path('users_of_vender/<int:user_id>', views.users_of_vender,name='users_of_vender'),
    path('users_of_vender_pagination/<int:user_id>/<int:page_number>', views.users_of_vender_pagination,name='users_of_vender_pagination'),

    path('view_aao_user_order/<int:aao_user_id>', views.view_aao_user_order,name='view_aao_user_order'),
    path('view_aao_user_order_pagination/<int:aao_user_id>/<int:page_number>', views.view_aao_user_order_pagination,name='view_aao_user_order_pagination'),



]
