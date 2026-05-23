from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse  # NEW: Import this so we can send background responses
import random

from .models import Cafeteria, Report, Notification, Ingredient, Inventory, Order, Menu, MealPlan
from .forms import CafeteriaForm, ReportForm, UserUpdateForm, OrderForm


@login_required
def index(request):
    cafeterias = Cafeteria.objects.all()
    reports = Report.objects.all().order_by('-date_generated')
    notifications = Notification.objects.filter(status='Unread').order_by('-date')
    return render(request, 'operations/index.html', {
        'cafeterias': cafeterias, 'reports': reports, 'notifications': notifications
    })


@login_required
def manage_cafeteria(request, cafe_id):
    cafe = get_object_or_404(Cafeteria, id=cafe_id)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'menu':
            Menu.objects.create(cafeteria=cafe, name=request.POST.get('name'),
                                description=request.POST.get('description'))
            messages.success(request, "Menu added successfully!")

        elif form_type == 'mealplan':
            MealPlan.objects.create(cafeteria=cafe, name=request.POST.get('name'), price=request.POST.get('price'))
            messages.success(request, "Meal Plan added successfully!")

        elif form_type == 'inventory':
            ing_name = request.POST.get('ingredient_name')
            qty = int(request.POST.get('quantity'))
            ingredient, _ = Ingredient.objects.get_or_create(name=ing_name)
            inv, created = Inventory.objects.get_or_create(cafeteria=cafe, ingredient=ingredient)
            inv.quantity = qty if created else inv.quantity + qty
            inv.save()

            # TRIGGER INVENTORY ALERT IF LOW
            if inv.quantity < 10:
                Notification.objects.create(inventory=inv, status='Unread')
                messages.warning(request, f"Low stock alert triggered for {ingredient.name}!")
            else:
                messages.success(request, "Inventory updated!")

        return redirect('manage_cafeteria', cafe_id=cafe.id)

    return render(request, 'operations/manage_cafeteria.html', {'cafe': cafe})


@login_required
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            Notification.objects.create(order=new_order, status='Unread')
            messages.success(request, "Order placed and notification generated.")
            return redirect('index')
    else:
        form = OrderForm()
    return render(request, 'operations/addOrder.html', {'form': form})



@login_required
def read_notification(request, notif_id):
    try:
        notif = Notification.objects.get(id=notif_id)
        notif.status = 'Read'
        notif.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required
def read_all_notifications(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        Notification.objects.filter(status='Unread').update(status='Read')
        return JsonResponse({'success': True})
    return redirect('index')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'operations/edit_profile.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        messages.error(request, "Invalid credentials.")
    return render(request, 'operations/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def add_cafeteria(request):
    if request.method == 'POST':
        form = CafeteriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CafeteriaForm()
    return render(request, 'operations/addNewCafeteria.html', {'form': form})


@login_required
def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            new_report = form.save()
            Notification.objects.create(report=new_report, status='Unread')
            return redirect('index')
    else:
        form = ReportForm()
    return render(request, 'operations/addNewReport.html', {'form': form})