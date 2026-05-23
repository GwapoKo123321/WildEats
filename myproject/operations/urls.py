from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('EditProfile/', views.edit_profile, name='edit_profile'),

    # Core Entity Forms
    path('AddCafeteria/', views.add_cafeteria, name='add_cafeteria'),
    path('AddReport/', views.add_report, name='add_report'),
    path('AddOrder/', views.add_order, name='add_order'),

    # Manage Cafeteria Page
    path('ManageCafeteria/<int:cafe_id>/', views.manage_cafeteria, name='manage_cafeteria'),

    # Notifications
    path('ReadNotification/<int:notif_id>/', views.read_notification, name='read_notification'),
    path('ReadAllNotifications/', views.read_all_notifications, name='read_all_notifications'),
]