from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Cafeteria, Report, Notification
from .forms import CafeteriaForm, ReportForm

def index(request):
    cafeterias = Cafeteria.objects.all()
    reports = Report.objects.all().order_by('-date_generated')
    notifications = Notification.objects.all().order_by('-date')
    context = {
        'cafeterias': cafeterias,
        'reports': reports,
        'notifications': notifications
    }
    return render(request, 'operations/index.html', context)

def add_cafeteria(request):
    if request.method == 'POST':
        form = CafeteriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CafeteriaForm()
    return render(request, 'operations/addNewCafeteria.html', {'form': form})

def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ReportForm()
    return render(request, 'operations/addNewReport.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        user_val = request.POST.get('username')
        pass_val = request.POST.get('password')
        user = authenticate(request, username=user_val, password=pass_val)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'operations/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')