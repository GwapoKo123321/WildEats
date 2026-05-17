from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Order, OrderItem, PaymentRecord


class SalesTransactionRoleFlowTests(TestCase):
    def setUp(self):
        self.student_group = Group.objects.create(name="student")
        self.vendor_group = Group.objects.create(name="vendor")
        self.admin_group = Group.objects.create(name="admin")

        self.student = User.objects.create_user(username="student", password="test-password")
        self.vendor = User.objects.create_user(username="vendor", password="test-password")
        self.admin = User.objects.create_user(username="admin", password="test-password")

        self.student.groups.add(self.student_group)
        self.vendor.groups.add(self.vendor_group)
        self.admin.groups.add(self.admin_group)

    def test_student_vendor_admin_demo_flow(self):
        self.client.force_login(self.student)

        order_response = self.client.post(
            reverse("add_new_order"),
            {"CustomerName": "Student One"}
        )
        order = Order.objects.get(CustomerName="Student One")
        self.assertRedirects(order_response, reverse("order_summary", args=[order.OrderID]))
        self.assertEqual(order.Student, self.student)
        self.assertEqual(order.TotalCost, Decimal("0.00"))
        self.assertEqual(order.OrderStatus, Order.STATUS_PENDING_PAYMENT)

        item_response = self.client.post(
            reverse("add_order_item", args=[order.OrderID]),
            {
                "ProductName": "Chicken Rice",
                "Quantity": 2,
                "Price": "85.00",
            }
        )
        self.assertRedirects(item_response, reverse("order_summary", args=[order.OrderID]))
        order.refresh_from_db()
        self.assertEqual(order.TotalCost, Decimal("170.00"))
        self.assertEqual(order.OrderStatus, Order.STATUS_PENDING_PAYMENT)

        payment_response = self.client.post(
            reverse("record_payment", args=[order.OrderID]),
            {
                "Amount": "170.00",
                "PaymentMethod": "Cash",
            }
        )
        self.assertRedirects(payment_response, reverse("order_summary", args=[order.OrderID]))
        payment = PaymentRecord.objects.get(Order=order)
        order.refresh_from_db()
        self.assertEqual(payment.PaymentStatus, PaymentRecord.STATUS_PENDING)
        self.assertEqual(order.OrderStatus, Order.STATUS_PAYMENT_SUBMITTED)

        self.client.force_login(self.vendor)
        vendor_dashboard = self.client.get(reverse("sales_home"))
        self.assertContains(vendor_dashboard, "Orders for Verification")
        self.assertContains(vendor_dashboard, "Order Details")

        verify_response = self.client.post(
            reverse("verify_payment", args=[order.OrderID, payment.PaymentID])
        )
        self.assertRedirects(verify_response, reverse("order_summary", args=[order.OrderID]))
        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.PaymentStatus, PaymentRecord.STATUS_VERIFIED)
        self.assertEqual(order.Vendor, self.vendor)
        self.assertEqual(order.TotalPaid, Decimal("170.00"))
        self.assertEqual(order.OrderStatus, Order.STATUS_PAYMENT_VERIFIED)

        processing_response = self.client.post(
            reverse("update_order_status", args=[order.OrderID]),
            {"status": Order.STATUS_PROCESSING}
        )
        self.assertRedirects(processing_response, reverse("order_summary", args=[order.OrderID]))
        order.refresh_from_db()
        self.assertEqual(order.OrderStatus, Order.STATUS_PROCESSING)

        completed_response = self.client.post(
            reverse("update_order_status", args=[order.OrderID]),
            {"status": Order.STATUS_COMPLETED}
        )
        self.assertRedirects(completed_response, reverse("order_summary", args=[order.OrderID]))
        order.refresh_from_db()
        self.assertEqual(order.OrderStatus, Order.STATUS_COMPLETED)

        self.client.force_login(self.admin)
        admin_dashboard = self.client.get(reverse("sales_home"))
        self.assertContains(admin_dashboard, "Admin Dashboard")
        self.assertContains(admin_dashboard, "Payment Records")
        self.assertContains(admin_dashboard, "Completed")

    def test_student_can_only_view_own_orders(self):
        other_student = User.objects.create_user(username="other", password="test-password")
        other_student.groups.add(self.student_group)
        order = Order.objects.create(CustomerName="Other Student", Student=other_student)

        self.client.force_login(self.student)
        response = self.client.get(reverse("order_summary", args=[order.OrderID]))

        self.assertEqual(response.status_code, 403)

    def test_student_can_delete_own_order(self):
        order = Order.objects.create(CustomerName="Delete Me", Student=self.student)

        self.client.force_login(self.student)
        response = self.client.post(reverse("delete_order", args=[order.OrderID]))

        self.assertRedirects(response, reverse("sales_home"))
        self.assertFalse(Order.objects.filter(OrderID=order.OrderID).exists())

    def test_student_cannot_delete_another_students_order(self):
        other_student = User.objects.create_user(username="other-delete", password="test-password")
        other_student.groups.add(self.student_group)
        order = Order.objects.create(CustomerName="Keep Me", Student=other_student)

        self.client.force_login(self.student)
        response = self.client.post(reverse("delete_order", args=[order.OrderID]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Order.objects.filter(OrderID=order.OrderID).exists())

    def test_vendor_can_see_pending_student_orders(self):
        order = Order.objects.create(
            CustomerName="Pending Student",
            Student=self.student,
            OrderStatus=Order.STATUS_PENDING_PAYMENT,
        )

        self.client.force_login(self.vendor)
        dashboard = self.client.get(reverse("sales_home"))
        details = self.client.get(reverse("order_summary", args=[order.OrderID]))

        self.assertContains(dashboard, "Pending Student")
        self.assertEqual(details.status_code, 200)

    def test_vendor_cannot_create_student_order(self):
        self.client.force_login(self.vendor)

        response = self.client.post(reverse("add_new_order"), {"CustomerName": "Blocked"})

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Order.objects.filter(CustomerName="Blocked").exists())

    def test_record_payment_rejects_amount_above_total_cost(self):
        self.client.force_login(self.student)
        order = Order.objects.create(CustomerName="Over Pay", Student=self.student)
        OrderItem.objects.create(
            Order=order,
            ProductName="Meal",
            Quantity=1,
            Price="100.00"
        )
        order.recompute_totals()

        response = self.client.post(
            reverse("record_payment", args=[order.OrderID]),
            {
                "Amount": "101.00",
                "PaymentMethod": "Cash",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Payment cannot exceed the remaining payable amount")
        self.assertEqual(PaymentRecord.objects.filter(Order=order).count(), 0)

    def test_reject_payment_sets_payment_and_order_status(self):
        order = Order.objects.create(
            CustomerName="Reject Me",
            Student=self.student,
            OrderStatus=Order.STATUS_PAYMENT_SUBMITTED,
        )
        OrderItem.objects.create(
            Order=order,
            ProductName="Meal",
            Quantity=1,
            Price="100.00"
        )
        payment = PaymentRecord.objects.create(
            Order=order,
            Amount="100.00",
            PaymentMethod="Cash",
            PaymentStatus=PaymentRecord.STATUS_PENDING,
        )
        order.recompute_totals()
        order.OrderStatus = Order.STATUS_PAYMENT_SUBMITTED
        order.save(update_fields=["OrderStatus"])

        self.client.force_login(self.vendor)
        response = self.client.post(reverse("reject_payment", args=[order.OrderID, payment.PaymentID]))

        self.assertRedirects(response, reverse("order_summary", args=[order.OrderID]))
        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.PaymentStatus, PaymentRecord.STATUS_REJECTED)
        self.assertEqual(order.OrderStatus, Order.STATUS_PAYMENT_REJECTED)
