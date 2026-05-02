from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render


@login_required
def index(request):
    return render(request, "index.html")


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session["username"] = self.request.user.username
        return response


@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        username = request.POST.get("username", "").strip()

        if not username:
            messages.error(request, "Username is required.")
            return redirect("edit_profile")

        username_exists = User.objects.exclude(pk=user.pk).filter(username=username).exists()
        if username_exists:
            messages.error(request, "That username is already taken.")
            return redirect("edit_profile")

        user.username = username
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()
        user.email = request.POST.get("email", "").strip()
        user.save()
        request.session["username"] = user.username
        messages.success(request, "Profile updated.")
        return redirect("edit_profile")

    return render(request, "edit_profile.html")


@login_required
def add_new_record(request):
    return redirect("add_new_order")


def log_off(request):
    request.session.flush()
    logout(request)
    return redirect("login")
