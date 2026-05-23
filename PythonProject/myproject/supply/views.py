from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ingredient, Inventory, Supplier
from .forms import IngredientForm, InventoryForm, SupplierForm, UserProfileForm


@login_required
def index(request):
    ingredients = Ingredient.objects.select_related('supplier').all().order_by('name')
    inventory_items = Inventory.objects.select_related('ingredient').all().order_by('ingredient__name')
    suppliers = Supplier.objects.all().order_by('name')

    return render(request, 'supply/index.html', {
        'ingredients': ingredients,
        'inventory_items': inventory_items,
        'suppliers': suppliers,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user_val = request.POST.get('username')
        pass_val = request.POST.get('password')
        user = authenticate(request, username=user_val, password=pass_val)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'supply/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('index')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'supply/editProfile.html', {'form': form})


@login_required
def add_new_record(request):
    return render(request, 'supply/addNewRecord.html')


@login_required
def add_new_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New supplier record added successfully.")
            return redirect('index')
    else:
        form = SupplierForm()

    return render(request, 'supply/addNewSupplier.html', {'form': form})


@login_required
def add_new_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New ingredient record added successfully.")
            return redirect('index')
    else:
        form = IngredientForm()

    return render(request, 'supply/addNewIngredient.html', {'form': form})


@login_required
def add_new_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New inventory record added successfully.")
            return redirect('index')
    else:
        form = InventoryForm()

    return render(request, 'supply/addNewInventory.html', {'form': form})
