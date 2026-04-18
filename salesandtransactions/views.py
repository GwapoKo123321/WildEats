from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order
from .forms import OrderItemForm
from django.contrib.auth.decorators import login_required
@login_required
def sales_home(request):
    orders = Order.objects.all()
    return render(request, 'salesandtransactions/home.html', {'orders': orders})


@login_required
def add_new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/sales/')  # after saving
    else:
        form = OrderForm()

    return render(request, 'salesandtransactions/addNewOrder.html', {'form': form})


@login_required
def add_order_item(request, order_id):
    order = Order.objects.get(OrderID=order_id)

    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.Order = order
            item.save()
            return redirect('/sales/')
    else:
        form = OrderItemForm()

    return render(request, 'salesandtransactions/addNewOrderItem.html', {
        'form': form,
        'order': order
    })