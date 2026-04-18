from django.contrib import admin
from django.urls import path, include
from supply import views as supply_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', supply_views.index, name='home'),
    path('WildEats/', include('supply.urls')),
]
