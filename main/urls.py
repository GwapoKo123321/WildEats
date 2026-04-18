from django.urls import path
from .views import index
from .views import index, CustomLoginView
urlpatterns = [
    path('', index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
]