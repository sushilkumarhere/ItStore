from . import views
from django.urls import path


urlpatterns = [
    # main Site URLs
    path('cpanel/', views.cpanel, name='cpanel'),
    path('', views.home, name='home'),
    path('system/', views.item_list, name='computer_list'),
    path('excel/', views.export_users_xls, name='export_users_xls'),
    path('labs/', views.labs, name='labs'),

    # Control Panel Site URLs
    path('cpanel/', views.cpanel, name='cpanel'),
    path('SignOut/', views.signout, name='SignOut'),
    path('cpanel/AdminItems/', views.citem_list, name='item_list'),
    path('cpanel/CreateItemList/', views.create_item_list, name='create_item_list1'),
    path('ajax/load-ItemModel/', views.load_ItemModel, name='ajax_load_ItemModel'),
    path('cpanel/UpdateItemList/<int:item_id>', views.update_item_list, name='update_item_list'),
    path('cpanel/DeleteItem/<int:item_id>',views.delete_item, name='Deleteitem'),
    path('cpanel/approved/<int:item_id>', views.item_approved, name='item_approved'),
    path('cpanel/User/', views.new_user, name='NewUser'),
    path('cpanel/UpdateUser/', views.update_user_profile, name='userprofile'),
    path('cpanel/chart/', views.chart_bar, name='chart_bar'),
    path('cpanel/chart1/', views.chart_bar1, name='chart_bar1'),

]
