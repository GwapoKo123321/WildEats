from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-new-record/', views.add_new_record, name='add_new_record'),
    path('add-new-ingredient/', views.add_new_ingredient, name='add_new_ingredient'),
    path('add-new-inventory/', views.add_new_inventory, name='add_new_inventory'),
    path('add-new-supplier/', views.add_new_supplier, name='add_new_supplier'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
