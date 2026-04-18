from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    from django.contrib.auth.decorators import login_required

@login_required
def index(request):
        return render(request, 'index.html')