from django.urls import path

from .views import CustomLoginView, HomePageView, add_new_record, edit_profile, log_off, register


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("add-new-record/", add_new_record, name="add_new_record"),
    path("logout/", log_off, name="logout"),
]
