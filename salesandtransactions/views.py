from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import MenuItemForm, OrderForm, OrderItemForm, PaymentRecordForm
from .models import MenuItem, Order, OrderItem, PaymentRecord
from .roles import ROLE_ADMIN, ROLE_STUDENT, ROLE_VENDOR, is_admin, is_student, is_vendor, user_role


def visible_orders_for(user):
    role = user_role(user)
    orders = Order.objects.select_related("Student", "Vendor").prefetch_related(
        "items",
        "items__MenuItem",
        "payments",
    )

    if role == ROLE_ADMIN:
        return orders.order_by("-OrderDate")
    if role == ROLE_VENDOR:
        return orders.filter(
            Q(Vendor=user) |
            Q(items__MenuItem__vendor=user) |
            Q(Vendor__isnull=True, OrderStatus=Order.STATUS_PAYMENT_SUBMITTED)
        ).distinct().order_by("-OrderDate")
    return orders.filter(Student=user, is_deleted=False).order_by("-OrderDate")


def visible_menu_items_for(user):
    role = user_role(user)
    items = MenuItem.objects.select_related("vendor")

    if role == ROLE_ADMIN:
        return items.order_by("name")
    if role == ROLE_VENDOR:
        return items.filter(vendor=user).order_by("name")
    return items.filter(is_available=True).order_by("name")


def visible_payments_for(user):
    role = user_role(user)
    payments = PaymentRecord.objects.select_related(
        "Order",
        "Order__Student",
        "Order__Vendor",
        "VerifiedByVendor",
    )

    if role == ROLE_ADMIN:
        return payments.order_by("-PaymentDate")
    if role == ROLE_VENDOR:
        return payments.filter(
            Q(Order__Vendor=user) |
            Q(Order__items__MenuItem__vendor=user) |
            Q(Order__Vendor__isnull=True, Order__OrderStatus=Order.STATUS_PAYMENT_SUBMITTED)
        ).distinct().order_by("-PaymentDate")
    return payments.filter(Order__Student=user).order_by("-PaymentDate")


def get_visible_order_or_403(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related("Student", "Vendor").prefetch_related(
            "items",
            "items__MenuItem",
            "payments",
        ),
        OrderID=order_id,
    )
    role = user_role(request.user)

    if role == ROLE_ADMIN:
        return order
    if role == ROLE_VENDOR and (
        order.Vendor_id == request.user.id
        or order.Vendor_id is None
        or order.items.filter(MenuItem__vendor=request.user).exists()
    ):
        return order
    if role == ROLE_STUDENT and order.Student_id == request.user.id and not order.is_deleted:
        return order
    return None


def render_order_details(request, order, item_form=None, payment_form=None):
    order = get_object_or_404(
        Order.objects.select_related("Student", "Vendor").prefetch_related(
            "items",
            "items__MenuItem",
            "payments",
        ),
        OrderID=order.OrderID,
    )
    role = user_role(request.user)

    if item_form is None:
        item_form = OrderItemForm()
    if payment_form is None:
        suggested_amount = order.TotalCost if order.TotalCost > 0 else 0
        payment_form = PaymentRecordForm(order=order, initial={"Amount": suggested_amount})
    latest_payment = order.payments.order_by("-PaymentDate").first()

    return render(request, "salesandtransactions/orderSummary.html", {
        "order": order,
        "payment_status": latest_payment.PaymentStatus if latest_payment else "No Payment",
        "item_form": item_form,
        "payment_form": payment_form,
        "role": role,
        "is_student": role == ROLE_STUDENT,
        "is_vendor": role == ROLE_VENDOR,
        "is_admin": role == ROLE_ADMIN,
        "can_modify_order": not order.is_inactive and order.OrderStatus in [
            Order.STATUS_PENDING_PAYMENT,
            Order.STATUS_PAYMENT_FAILED,
        ],
        "can_cancel_order": order.can_cancel,
    })


@login_required
def sales_home(request):
    role = user_role(request.user)
    orders = visible_orders_for(request.user)
    payments = visible_payments_for(request.user)
    users = []
    vendors = []
    menu_items = visible_menu_items_for(request.user)

    if role == ROLE_ADMIN:
        from django.contrib.auth.models import User

        users = User.objects.filter(groups__name=ROLE_STUDENT).order_by("username")
        vendors = User.objects.filter(groups__name=ROLE_VENDOR).order_by("username")

    return render(request, "salesandtransactions/home.html", {
        "orders": orders,
        "payments": payments,
        "users": users,
        "vendors": vendors,
        "menu_items": menu_items,
        "role": role,
        "is_student": role == ROLE_STUDENT,
        "is_vendor": role == ROLE_VENDOR,
        "is_admin": role == ROLE_ADMIN,
    })


@login_required
def add_new_order(request):
    if is_vendor(request.user):
        return HttpResponseForbidden("Vendors cannot create student orders.")

    if request.method == "POST":
        form = OrderForm(request.POST)
        item_form = OrderItemForm(request.POST)
        if form.is_valid() and item_form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.Student = request.user
                order.OrderStatus = Order.STATUS_PENDING_PAYMENT
                order.save()

                menu_item = item_form.cleaned_data["menu_item"]
                item = item_form.save(commit=False)
                item.Order = order
                item.MenuItem = menu_item
                item.ProductName = menu_item.name
                item.Price = menu_item.price
                item.save()
                order.recompute_totals()
            return redirect("order_summary", order_id=order.OrderID)
    else:
        initial_name = request.user.get_full_name() or request.user.username
        form = OrderForm(initial={"CustomerName": initial_name})
        item_form = OrderItemForm()

    return render(request, "salesandtransactions/addNewOrder.html", {
        "form": form,
        "item_form": item_form,
    })


@login_required
def menu_items(request):
    return render(request, "salesandtransactions/menuItems.html", {
        "menu_items": visible_menu_items_for(request.user),
        "is_student": is_student(request.user),
        "is_vendor": is_vendor(request.user),
        "is_admin": is_admin(request.user),
    })


@login_required
def payment_records(request):
    return render(request, "salesandtransactions/paymentRecords.html", {
        "payments": visible_payments_for(request.user),
        "is_student": is_student(request.user),
        "is_vendor": is_vendor(request.user),
        "is_admin": is_admin(request.user),
    })


@login_required
def registered_students(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only admins can view registered students.")

    from django.contrib.auth.models import User

    return render(request, "salesandtransactions/registeredUsers.html", {
        "title": "Registered Students",
        "users": User.objects.filter(groups__name=ROLE_STUDENT).order_by("username"),
        "is_student": False,
        "is_vendor": False,
        "is_admin": True,
    })


@login_required
def registered_vendors(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only admins can view registered vendors.")

    from django.contrib.auth.models import User

    return render(request, "salesandtransactions/registeredUsers.html", {
        "title": "Registered Vendors",
        "users": User.objects.filter(groups__name=ROLE_VENDOR).order_by("username"),
        "is_student": False,
        "is_vendor": False,
        "is_admin": True,
    })


@login_required
def add_menu_item(request):
    if not is_vendor(request.user) and not is_admin(request.user):
        return HttpResponseForbidden("Only vendors can add menu items.")

    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.vendor = request.user
            item.save()
            messages.success(request, "Menu item saved.")
            return redirect("menu_items")
    else:
        form = MenuItemForm()

    return render(request, "salesandtransactions/menuItemForm.html", {
        "form": form,
        "title": "Add Menu Item",
        "is_student": is_student(request.user),
        "is_vendor": is_vendor(request.user),
        "is_admin": is_admin(request.user),
    })


@login_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, MenuItemID=item_id)
    if not is_admin(request.user) and item.vendor_id != request.user.id:
        return HttpResponseForbidden("You cannot edit this menu item.")

    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated.")
            return redirect("menu_items")
    else:
        form = MenuItemForm(instance=item)

    return render(request, "salesandtransactions/menuItemForm.html", {
        "form": form,
        "title": "Edit Menu Item",
        "item": item,
        "is_student": is_student(request.user),
        "is_vendor": is_vendor(request.user),
        "is_admin": is_admin(request.user),
    })


@login_required
@require_POST
def disable_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, MenuItemID=item_id)
    if not is_admin(request.user) and item.vendor_id != request.user.id:
        return HttpResponseForbidden("You cannot disable this menu item.")

    item.is_available = False
    item.save(update_fields=["is_available", "updated_at"])
    messages.success(request, "Menu item disabled.")
    return redirect("menu_items")


@login_required
@require_POST
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, MenuItemID=item_id)
    if not is_admin(request.user) and item.vendor_id != request.user.id:
        return HttpResponseForbidden("You cannot delete this menu item.")

    if OrderItem.objects.filter(MenuItem=item).exists():
        item.is_available = False
        item.save(update_fields=["is_available", "updated_at"])
        messages.success(request, "Menu item is used in order history, so it was disabled instead.")
    else:
        item.delete()
        messages.success(request, "Menu item deleted.")
    return redirect("menu_items")


@login_required
def add_order_item(request, order_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if order.is_inactive:
        return HttpResponseForbidden("Cancelled orders cannot be edited.")
    if not (is_student(request.user) and order.Student_id == request.user.id) and not is_admin(request.user):
        return HttpResponseForbidden("Only the student who owns this order can add items.")
    if order.OrderStatus not in [Order.STATUS_PENDING_PAYMENT, Order.STATUS_PAYMENT_FAILED]:
        messages.error(request, "Items can only be changed before payment is accepted for verification.")
        return redirect("order_summary", order_id=order.OrderID)

    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            menu_item = form.cleaned_data["menu_item"]
            item = form.save(commit=False)
            item.Order = order
            item.MenuItem = menu_item
            item.ProductName = menu_item.name
            item.Price = menu_item.price
            item.save()
            order.recompute_totals()
            if order.OrderStatus == Order.STATUS_PAYMENT_FAILED:
                order.OrderStatus = Order.STATUS_PENDING_PAYMENT
                order.save(update_fields=["OrderStatus"])
            return redirect("order_summary", order_id=order.OrderID)
        return render_order_details(request, order, item_form=form)

    return redirect("order_summary", order_id=order.OrderID)


@login_required
def record_payment(request, order_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if order.is_inactive:
        return HttpResponseForbidden("Cancelled orders cannot accept payments.")
    if not (is_student(request.user) and order.Student_id == request.user.id) and not is_admin(request.user):
        return HttpResponseForbidden("Only the student who owns this order can submit payment.")
    if order.TotalCost <= 0:
        messages.error(request, "Add at least one item before submitting payment.")
        return redirect("order_summary", order_id=order.OrderID)
    if order.OrderStatus not in [Order.STATUS_PENDING_PAYMENT, Order.STATUS_PAYMENT_FAILED]:
        messages.error(request, "Payment has already been submitted for this order.")
        return redirect("order_summary", order_id=order.OrderID)

    if request.method == "POST":
        form = PaymentRecordForm(request.POST, order=order)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.Order = order
            payment.PaymentMethod = "Cash"
            payment.CashPayment = True
            payment.PaymentStatus = PaymentRecord.STATUS_PENDING
            payment.save()
            order.OrderStatus = Order.STATUS_PAYMENT_SUBMITTED
            order.save(update_fields=["OrderStatus"])
            return redirect("order_summary", order_id=order.OrderID)
        return render_order_details(request, order, payment_form=form)

    return redirect("order_summary", order_id=order.OrderID)


@login_required
def order_summary(request, order_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    return render_order_details(request, order)


@login_required
@require_http_methods(["GET", "POST"])
def delete_order_item(request, order_id, item_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if order.is_inactive:
        return HttpResponseForbidden("Cancelled orders cannot be verified.")
    if not (is_student(request.user) and order.Student_id == request.user.id) and not is_admin(request.user):
        return HttpResponseForbidden("Only the student who owns this order can delete items.")
    if order.OrderStatus not in [Order.STATUS_PENDING_PAYMENT, Order.STATUS_PAYMENT_FAILED]:
        messages.error(request, "Items can only be changed before payment is accepted for verification.")
        return redirect("order_summary", order_id=order.OrderID)

    item = get_object_or_404(OrderItem, Order=order, OrderItemID=item_id)
    item.delete()
    order.recompute_totals()
    if not order.items.exists() and order.can_cancel:
        order.cancel()
        messages.success(request, "Order was cancelled because it has no items.")
        return redirect("sales_home")
    return redirect("order_summary", order_id=order.OrderID)


@login_required
@require_POST
def verify_payment(request, order_id, payment_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if order.is_inactive:
        return HttpResponseForbidden("Cancelled orders cannot be verified.")
    if not is_vendor(request.user) and not is_admin(request.user):
        return HttpResponseForbidden("Only vendors can verify payments.")

    payment = get_object_or_404(PaymentRecord, Order=order, PaymentID=payment_id)
    payment.PaymentStatus = PaymentRecord.STATUS_VERIFIED
    payment.VerifiedByVendor = request.user
    payment.save(update_fields=["PaymentStatus", "VerifiedByVendor"])
    if is_vendor(request.user) and order.Vendor_id is None:
        order.Vendor = request.user
    order.OrderStatus = Order.STATUS_PAYMENT_VERIFIED
    order.save(update_fields=["Vendor", "OrderStatus"])
    order.recompute_totals()
    return redirect("order_summary", order_id=order.OrderID)


@login_required
@require_POST
def fail_payment(request, order_id, payment_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if order.is_inactive:
        return HttpResponseForbidden("Cancelled orders cannot be updated.")
    if not is_vendor(request.user) and not is_admin(request.user):
        return HttpResponseForbidden("Only vendors can fail payments.")

    payment = get_object_or_404(PaymentRecord, Order=order, PaymentID=payment_id)
    payment.PaymentStatus = PaymentRecord.STATUS_FAILED
    payment.VerifiedByVendor = request.user
    payment.save(update_fields=["PaymentStatus", "VerifiedByVendor"])
    if is_vendor(request.user) and order.Vendor_id is None:
        order.Vendor = request.user
    order.OrderStatus = Order.STATUS_PAYMENT_FAILED
    order.save(update_fields=["Vendor", "OrderStatus"])
    order.recompute_totals()
    return redirect("order_summary", order_id=order.OrderID)


@login_required
@require_POST
def update_order_status(request, order_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if order.is_inactive:
        return HttpResponseForbidden("Cancelled orders cannot be updated.")
    if not is_vendor(request.user) and not is_admin(request.user):
        return HttpResponseForbidden("Only vendors can update order status.")

    next_status = request.POST.get("status")
    allowed_statuses = [Order.STATUS_PROCESSING, Order.STATUS_COMPLETED]
    if next_status not in allowed_statuses:
        messages.error(request, "Invalid order status update.")
        return redirect("order_summary", order_id=order.OrderID)

    if is_vendor(request.user) and order.Vendor_id is None:
        order.Vendor = request.user
    order.OrderStatus = next_status
    order.save(update_fields=["Vendor", "OrderStatus"])
    return redirect("order_summary", order_id=order.OrderID)


@login_required
@require_POST
def delete_order(request, order_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if not is_admin(request.user) and not (is_student(request.user) and order.Student_id == request.user.id):
        return HttpResponseForbidden("You cannot delete this order.")
    try:
        order.cancel()
    except ValidationError:
        messages.error(request, "Orders linked to payment records cannot be cancelled.")
        return redirect("order_summary", order_id=order.OrderID)
    return redirect("sales_home")
