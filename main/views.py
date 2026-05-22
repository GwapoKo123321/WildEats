from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views import View


ROLE_CHOICES = {"student", "vendor", "admin"}
ROLE_GROUP_NAMES = tuple(ROLE_CHOICES)


def apply_role_permissions(user, role):
    user.is_staff = False
    user.is_superuser = False

    if role == "vendor":
        user.is_staff = True

    elif role == "admin":
        user.is_staff = True
        user.is_superuser = True


def set_single_role(user, role):
    Group.objects.get_or_create(name="student")
    Group.objects.get_or_create(name="vendor")
    Group.objects.get_or_create(name="admin")
    user.groups.remove(*Group.objects.filter(name__in=ROLE_GROUP_NAMES))
    group = Group.objects.get(name=role)
    user.groups.add(group)


def sync_role_flags(user):
    if user.groups.filter(name="admin").exists():
        user.groups.remove(*Group.objects.filter(name__in=("student", "vendor")))
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_superuser"])
        return

    if user.groups.filter(name="student").exists():
        user.groups.remove(*Group.objects.filter(name__in=("vendor",)))
        user.is_staff = False
        user.is_superuser = False
        user.save(update_fields=["is_staff", "is_superuser"])
        return

    if user.groups.filter(name="vendor").exists():
        user.is_staff = True
        user.is_superuser = False
        user.save(update_fields=["is_staff", "is_superuser"])


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return "/sales/"

    def form_valid(self, form):
        user = form.get_user()
        sync_role_flags(user)

        response = super().form_valid(form)
        self.request.session["username"] = self.request.user.username
        return response


def _style_registration_form(form):
    form.fields["username"].widget.attrs.update({
        "placeholder": "Choose a username",
        "autocomplete": "username",
    })
    form.fields["password1"].widget.attrs.update({
        "placeholder": "Password",
        "autocomplete": "new-password",
    })
    form.fields["password2"].widget.attrs.update({
        "placeholder": "Repeat password",
        "autocomplete": "new-password",
    })


def registration_context(form, role="", request_data=None):
    request_data = request_data or {}
    return {
        "form": form,
        "role": role,
        "first_name": request_data.get("first_name", ""),
        "last_name": request_data.get("last_name", ""),
        "email": request_data.get("email", ""),
    }


def register(request):
    if request.user.is_authenticated:
        return redirect("sales_home")

    submitted_role = request.POST.get("role") or request.GET.get("role")
    role = submitted_role or ""

    if submitted_role is not None and role not in ROLE_CHOICES:
        messages.error(request, "Please select a valid registration type.")
        return redirect("register")

    if request.method == "POST":
        if not role:
            messages.error(request, "Please select a registration type.")
            return redirect("register")

        form = UserCreationForm(request.POST)
        _style_registration_form(form)

        username = request.POST.get("username", "").strip()

        if User.objects.filter(username__iexact=username).exists():
            form.add_error("username", "Username already exists. Please choose another one.")
            messages.error(request, "Username already exists. Please choose another one.")
            return render(request, "register.html", registration_context(form, role, request.POST))

        if form.is_valid():
            user = form.save(commit=False)

            user.first_name = request.POST.get("first_name", "").strip()
            user.last_name = request.POST.get("last_name", "").strip()
            user.email = request.POST.get("email", "").strip()

            apply_role_permissions(user, role)

            try:
                user.save()
                set_single_role(user, role)
            except IntegrityError:
                form.add_error("username", "Username already exists. Please choose another one.")
                messages.error(request, "Username already exists. Please choose another one.")
                return render(request, "register.html", registration_context(form, role, request.POST))

            messages.success(request, "Account created. You can now log in.")
            return redirect("login")

    else:
        form = UserCreationForm()
        _style_registration_form(form)

    return render(request, "register.html", registration_context(form, role, request.POST if request.method == "POST" else None))


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


def log_off(request):
    request.session.flush()
    logout(request)
    return redirect("login")

class HomePageView(View):
    template_name = 'index.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("sales_home")

        user = request.user
        return render(request, self.template_name, {
            'user': user,
            'is_student': False,
            'is_vendor': False,
            'is_admin': False,
        })
