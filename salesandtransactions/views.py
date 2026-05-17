from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import OrderForm, OrderItemForm, PaymentRecordForm
from .models import Order, OrderItem, PaymentRecord
from .roles import ROLE_ADMIN, ROLE_STUDENT, ROLE_VENDOR, is_admin, is_student, is_vendor, user_role


def visible_orders_for(user):
    role = user_role(user)
    orders = Order.objects.select_related("Student", "Vendor").prefetch_related("items", "payments")

    if role == ROLE_ADMIN:
        return orders.order_by("-OrderDate")
    if role == ROLE_VENDOR:
        return orders.filter(
            Q(Vendor=user) | Q(Vendor__isnull=True)
        ).order_by("-OrderDate")
    return orders.filter(Student=user).order_by("-OrderDate")


def get_visible_order_or_403(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related("Student", "Vendor").prefetch_related("items", "payments"),
        OrderID=order_id,
    )
    role = user_role(request.user)

    if role == ROLE_ADMIN:
        return order
    if role == ROLE_VENDOR and (
        order.Vendor_id == request.user.id
        or order.Vendor_id is None
    ):
        return order
    if role == ROLE_STUDENT and order.Student_id == request.user.id:
        return order
    return None


def render_order_details(request, order, item_form=None, payment_form=None):
    order = get_object_or_404(
        Order.objects.select_related("Student", "Vendor").prefetch_related("items", "payments"),
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
    })


@login_required
def sales_home(request):
    role = user_role(request.user)
    orders = visible_orders_for(request.user)
    payments = PaymentRecord.objects.select_related("Order", "Order__Student", "Order__Vendor").order_by("-PaymentDate")
    users = []
    vendors = []

    if role == ROLE_ADMIN:
        from django.contrib.auth.models import User

        users = User.objects.filter(groups__name=ROLE_STUDENT).order_by("username")
        vendors = User.objects.filter(groups__name=ROLE_VENDOR).order_by("username")

    return render(request, "salesandtransactions/home.html", {
        "orders": orders,
        "payments": payments if role == ROLE_ADMIN else [],
        "users": users,
        "vendors": vendors,
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
        if form.is_valid():
            order = form.save(commit=False)
            order.Student = request.user
            order.OrderStatus = Order.STATUS_PENDING_PAYMENT
            order.save()
            order.recompute_totals()
            return redirect("order_summary", order_id=order.OrderID)
    else:
        initial_name = request.user.get_full_name() or request.user.username
        form = OrderForm(initial={"CustomerName": initial_name})

    return render(request, "salesandtransactions/addNewOrder.html", {"form": form})


@login_required
def add_order_item(request, order_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if not (is_student(request.user) and order.Student_id == request.user.id) and not is_admin(request.user):
        return HttpResponseForbidden("Only the student who owns this order can add items.")
    if order.OrderStatus not in [Order.STATUS_PENDING_PAYMENT, Order.STATUS_PAYMENT_REJECTED]:
        messages.error(request, "Items can only be changed before payment is accepted for verification.")
        return redirect("order_summary", order_id=order.OrderID)

    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.Order = order
            item.save()
            order.recompute_totals()
            if order.OrderStatus == Order.STATUS_PAYMENT_REJECTED:
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
    if not (is_student(request.user) and order.Student_id == request.user.id) and not is_admin(request.user):
        return HttpResponseForbidden("Only the student who owns this order can submit payment.")
    if order.TotalCost <= 0:
        messages.error(request, "Add at least one item before submitting payment.")
        return redirect("order_summary", order_id=order.OrderID)

    if request.method == "POST":
        form = PaymentRecordForm(request.POST, order=order)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.Order = order
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
@require_POST
def delete_order_item(request, order_id, item_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if not (is_student(request.user) and order.Student_id == request.user.id) and not is_admin(request.user):
        return HttpResponseForbidden("Only the student who owns this order can delete items.")
    if order.OrderStatus not in [Order.STATUS_PENDING_PAYMENT, Order.STATUS_PAYMENT_REJECTED]:
        messages.error(request, "Items can only be changed before payment is accepted for verification.")
        return redirect("order_summary", order_id=order.OrderID)

    item = get_object_or_404(OrderItem, Order=order, OrderItemID=item_id)
    item.delete()
    order.recompute_totals()
    return redirect("order_summary", order_id=order.OrderID)


@login_required
@require_POST
def verify_payment(request, order_id, payment_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if not is_vendor(request.user) and not is_admin(request.user):
        return HttpResponseForbidden("Only vendors can verify payments.")

    payment = get_object_or_404(PaymentRecord, Order=order, PaymentID=payment_id)
    payment.PaymentStatus = PaymentRecord.STATUS_VERIFIED
    payment.save(update_fields=["PaymentStatus"])
    if is_vendor(request.user) and order.Vendor_id is None:
        order.Vendor = request.user
    order.OrderStatus = Order.STATUS_PAYMENT_VERIFIED
    order.save(update_fields=["Vendor", "OrderStatus"])
    order.recompute_totals()
    return redirect("order_summary", order_id=order.OrderID)


@login_required
@require_POST
def reject_payment(request, order_id, payment_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
    if not is_vendor(request.user) and not is_admin(request.user):
        return HttpResponseForbidden("Only vendors can reject payments.")

    payment = get_object_or_404(PaymentRecord, Order=order, PaymentID=payment_id)
    payment.PaymentStatus = PaymentRecord.STATUS_REJECTED
    payment.save(update_fields=["PaymentStatus"])
    if is_vendor(request.user) and order.Vendor_id is None:
        order.Vendor = request.user
    order.OrderStatus = Order.STATUS_PAYMENT_REJECTED
    order.save(update_fields=["Vendor", "OrderStatus"])
    order.recompute_totals()
    return redirect("order_summary", order_id=order.OrderID)


@login_required
@require_POST
def update_order_status(request, order_id):
    order = get_visible_order_or_403(request, order_id)
    if order is None:
        return HttpResponseForbidden("You cannot access this order.")
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
    order.delete()
    return redirect("sales_home")
