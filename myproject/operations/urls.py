from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('EditProfile/', views.edit_profile, name='edit_profile'),
    path('AddCafeteria/', views.add_cafeteria, name='add_cafeteria'),
    path('AddReport/', views.add_report, name='add_report'),
]