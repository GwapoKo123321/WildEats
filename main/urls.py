from django.urls import path

from .views import CustomLoginView, add_new_record, edit_profile, index, log_off


urlpatterns = [
    path("", index, name="index"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("add-new-record/", add_new_record, name="add_new_record"),
    path("logout/", log_off, name="logout"),
]
