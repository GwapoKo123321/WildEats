from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import MenuItem, Order, OrderItem, PaymentRecord


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
        self.menu_item = MenuItem.objects.create(
            vendor=self.vendor,
            name="Chicken Rice",
            price="85.00",
            is_available=True,
        )

    def test_student_vendor_admin_demo_flow(self):
        self.client.force_login(self.student)

        order_response = self.client.post(
            reverse("add_new_order"),
            {
                "CustomerName": "Student One",
                "menu_item": self.menu_item.MenuItemID,
                "Quantity": 1,
            }
        )
        order = Order.objects.get(CustomerName="Student One")
        self.assertRedirects(order_response, reverse("order_summary", args=[order.OrderID]))
        self.assertEqual(order.Student, self.student)
        self.assertEqual(order.TotalCost, Decimal("85.00"))
        self.assertEqual(order.OrderStatus, Order.STATUS_PENDING_PAYMENT)
        self.assertEqual(order.items.count(), 1)

        item_response = self.client.post(
            reverse("add_order_item", args=[order.OrderID]),
            {
                "menu_item": self.menu_item.MenuItemID,
                "Quantity": 2,
            }
        )
        self.assertRedirects(item_response, reverse("order_summary", args=[order.OrderID]))
        order.refresh_from_db()
        item = order.items.order_by("-OrderItemID").first()
        self.assertEqual(item.ProductName, "Chicken Rice")
        self.assertEqual(item.Price, Decimal("85.00"))
        self.assertEqual(order.TotalCost, Decimal("255.00"))
        self.assertEqual(order.OrderStatus, Order.STATUS_PENDING_PAYMENT)

        payment_response = self.client.post(
            reverse("record_payment", args=[order.OrderID]),
            {
                "Amount": "255.00",
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
        self.assertEqual(payment.VerifiedByVendor, self.vendor)
        self.assertEqual(order.Vendor, self.vendor)
        self.assertEqual(order.TotalPaid, Decimal("255.00"))
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

    def test_clean_sales_routes_and_legacy_redirects(self):
        order = Order.objects.create(CustomerName="Route Check", Student=self.student)
        item = OrderItem.objects.create(
            Order=order,
            MenuItem=self.menu_item,
            ProductName=self.menu_item.name,
            Quantity=1,
            Price=self.menu_item.price,
        )

        self.assertEqual(reverse("add_new_order"), "/sales/orders/new/")
        self.assertEqual(reverse("order_summary", args=[order.OrderID]), f"/sales/orders/{order.OrderID}/")
        self.assertEqual(
            reverse("add_order_item", args=[order.OrderID]),
            f"/sales/orders/{order.OrderID}/items/add/",
        )
        self.assertEqual(
            reverse("delete_order_item", args=[order.OrderID, item.OrderItemID]),
            f"/sales/orders/{order.OrderID}/items/{item.OrderItemID}/delete/",
        )

        self.client.force_login(self.student)
        response = self.client.get(f"/sales/orderSummary/{order.OrderID}/")

        self.assertRedirects(
            response,
            reverse("order_summary", args=[order.OrderID]),
            fetch_redirect_response=False,
        )

    def test_student_can_delete_own_order(self):
        order = Order.objects.create(CustomerName="Delete Me", Student=self.student)

        self.client.force_login(self.student)
        response = self.client.post(reverse("delete_order", args=[order.OrderID]))

        self.assertRedirects(response, reverse("sales_home"))
        order.refresh_from_db()
        self.assertTrue(order.is_deleted)
        self.assertEqual(order.OrderStatus, Order.STATUS_CANCELLED)

    def test_order_summary_shows_order_information(self):
        order = Order.objects.create(CustomerName="Info View", Student=self.student)
        OrderItem.objects.create(
            Order=order,
            MenuItem=self.menu_item,
            ProductName=self.menu_item.name,
            Quantity=1,
            Price=self.menu_item.price,
        )
        order.recompute_totals()

        self.client.force_login(self.student)
        response = self.client.get(reverse("order_summary", args=[order.OrderID]))

        self.assertContains(response, "Customer: Info View")
        self.assertContains(response, "Student: student")
        self.assertContains(response, "Status: Pending Payment")
        self.assertContains(response, "Total: &#8369;85.00", html=True)
        self.assertContains(response, "Balance: &#8369;85.00", html=True)

    def test_admin_dashboard_links_to_payment_and_menu_sections(self):
        order = Order.objects.create(
            CustomerName="Dashboard Info",
            Student=self.student,
            OrderStatus=Order.STATUS_PAYMENT_SUBMITTED,
        )
        PaymentRecord.objects.create(
            Order=order,
            Amount="85.00",
            PaymentMethod="Cash",
            PaymentStatus=PaymentRecord.STATUS_PENDING,
        )

        self.client.force_login(self.admin)
        response = self.client.get(reverse("sales_home"))

        self.assertContains(response, f'href="{reverse("menu_items")}"')
        self.assertContains(response, f'href="{reverse("payment_records")}"')
        self.assertNotContains(response, 'id="menu-items-panel"')
        self.assertNotContains(response, 'id="payment-records-panel"')
        self.assertNotContains(response, "Chicken Rice")
        self.assertContains(response, "Dashboard Info")
        self.assertNotContains(response, "Cash")

        payments_response = self.client.get(reverse("payment_records"))
        self.assertContains(payments_response, "Dashboard Info")
        self.assertContains(payments_response, "Payment ID")
        self.assertContains(payments_response, "Order")
        self.assertContains(payments_response, "Cash")

    def test_admin_dashboard_links_to_registered_user_lists(self):
        self.student.first_name = "Student"
        self.student.last_name = "User"
        self.student.email = "student@example.com"
        self.student.save(update_fields=["first_name", "last_name", "email"])
        self.vendor.first_name = "Vendor"
        self.vendor.last_name = "User"
        self.vendor.email = "vendor@example.com"
        self.vendor.save(update_fields=["first_name", "last_name", "email"])

        self.client.force_login(self.admin)
        dashboard_response = self.client.get(reverse("sales_home"))
        students_response = self.client.get(reverse("registered_students"))
        vendors_response = self.client.get(reverse("registered_vendors"))

        self.assertContains(dashboard_response, f'href="{reverse("registered_students")}"')
        self.assertContains(dashboard_response, f'href="{reverse("registered_vendors")}"')
        self.assertContains(students_response, "Registered Students")
        self.assertContains(students_response, "Student User")
        self.assertContains(students_response, "student@example.com")
        self.assertContains(vendors_response, "Registered Vendors")
        self.assertContains(vendors_response, "Vendor User")
        self.assertContains(vendors_response, "vendor@example.com")

    def test_registered_user_lists_are_admin_only(self):
        self.client.force_login(self.student)
        students_response = self.client.get(reverse("registered_students"))

        self.client.force_login(self.vendor)
        vendors_response = self.client.get(reverse("registered_vendors"))

        self.assertEqual(students_response.status_code, 403)
        self.assertEqual(vendors_response.status_code, 403)

    def test_student_can_view_menu_items_and_own_payment_records(self):
        own_order = Order.objects.create(CustomerName="Own Payment", Student=self.student)
        own_payment = PaymentRecord.objects.create(
            Order=own_order,
            Amount="85.00",
            PaymentMethod="Cash",
            PaymentStatus=PaymentRecord.STATUS_PENDING,
        )
        other_student = User.objects.create_user(username="payment-other", password="test-password")
        other_student.groups.add(self.student_group)
        other_order = Order.objects.create(CustomerName="Other Payment", Student=other_student)
        PaymentRecord.objects.create(
            Order=other_order,
            Amount="40.00",
            PaymentMethod="Cash",
            PaymentStatus=PaymentRecord.STATUS_PENDING,
        )

        self.client.force_login(self.student)
        menu_response = self.client.get(reverse("menu_items"))
        payments_response = self.client.get(reverse("payment_records"))

        self.assertContains(menu_response, "Chicken Rice")
        self.assertNotContains(menu_response, "Edit")
        self.assertContains(payments_response, "Own Payment")
        self.assertContains(payments_response, f"<td>{own_payment.PaymentID}</td>", html=True)
        self.assertNotContains(payments_response, "Other Payment")

    def test_vendor_can_view_related_payment_records(self):
        vendor_order = Order.objects.create(CustomerName="Vendor Payment", Student=self.student)
        OrderItem.objects.create(
            Order=vendor_order,
            MenuItem=self.menu_item,
            ProductName=self.menu_item.name,
            Quantity=1,
            Price=self.menu_item.price,
        )
        PaymentRecord.objects.create(
            Order=vendor_order,
            Amount="85.00",
            PaymentMethod="Cash",
            PaymentStatus=PaymentRecord.STATUS_PENDING,
        )
        other_vendor = User.objects.create_user(username="other-vendor", password="test-password")
        other_vendor.groups.add(self.vendor_group)
        other_item = MenuItem.objects.create(vendor=other_vendor, name="Other Meal", price="40.00")
        other_order = Order.objects.create(CustomerName="Hidden Vendor Payment", Student=self.student)
        OrderItem.objects.create(
            Order=other_order,
            MenuItem=other_item,
            ProductName=other_item.name,
            Quantity=1,
            Price=other_item.price,
        )
        PaymentRecord.objects.create(
            Order=other_order,
            Amount="40.00",
            PaymentMethod="Cash",
            PaymentStatus=PaymentRecord.STATUS_PENDING,
        )

        self.client.force_login(self.vendor)
        response = self.client.get(reverse("payment_records"))

        self.assertContains(response, "Vendor Payment")
        self.assertNotContains(response, "Hidden Vendor Payment")

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
            OrderStatus=Order.STATUS_PAYMENT_SUBMITTED,
        )
        OrderItem.objects.create(
            Order=order,
            MenuItem=self.menu_item,
            ProductName=self.menu_item.name,
            Quantity=1,
            Price=self.menu_item.price,
        )

        self.client.force_login(self.vendor)
        dashboard = self.client.get(reverse("sales_home"))
        details = self.client.get(reverse("order_summary", args=[order.OrderID]))

        self.assertContains(dashboard, "Pending Student")
        self.assertEqual(details.status_code, 200)

    def test_student_dropdown_copies_menu_item_price_at_order_time(self):
        self.client.force_login(self.student)
        order = Order.objects.create(CustomerName="Snapshot", Student=self.student)

        response = self.client.post(
            reverse("add_order_item", args=[order.OrderID]),
            {
                "menu_item": self.menu_item.MenuItemID,
                "Quantity": 3,
            },
        )
        self.menu_item.price = Decimal("99.00")
        self.menu_item.save(update_fields=["price"])

        self.assertRedirects(response, reverse("order_summary", args=[order.OrderID]))
        item = OrderItem.objects.get(Order=order)
        order.refresh_from_db()
        self.assertEqual(item.ProductName, "Chicken Rice")
        self.assertEqual(item.Price, Decimal("85.00"))
        self.assertEqual(order.TotalCost, Decimal("255.00"))

    def test_vendor_can_manage_own_menu_items(self):
        self.client.force_login(self.vendor)

        create_response = self.client.post(reverse("add_menu_item"), {
            "name": "Cake",
            "description": "Slice",
            "price": "50.00",
            "is_available": "on",
        })
        item = MenuItem.objects.get(name="Cake")
        disable_response = self.client.post(reverse("disable_menu_item", args=[item.MenuItemID]))

        self.assertRedirects(create_response, reverse("menu_items"))
        self.assertRedirects(disable_response, reverse("menu_items"))
        item.refresh_from_db()
        self.assertEqual(item.vendor, self.vendor)
        self.assertFalse(item.is_available)

    def test_vendor_can_delete_unused_menu_item(self):
        item = MenuItem.objects.create(vendor=self.vendor, name="Unused", price="40.00")
        self.client.force_login(self.vendor)

        response = self.client.post(reverse("delete_menu_item", args=[item.MenuItemID]))

        self.assertRedirects(response, reverse("menu_items"))
        self.assertFalse(MenuItem.objects.filter(MenuItemID=item.MenuItemID).exists())

    def test_cancelled_order_blocks_payment_verification(self):
        order = Order.objects.create(
            CustomerName="Cancelled",
            Student=self.student,
            OrderStatus=Order.STATUS_CANCELLED,
            is_deleted=True,
        )
        payment = PaymentRecord.objects.create(
            Order=order,
            Amount="85.00",
            PaymentMethod="Cash",
            PaymentStatus=PaymentRecord.STATUS_PENDING,
        )

        self.client.force_login(self.vendor)
        response = self.client.post(reverse("verify_payment", args=[order.OrderID, payment.PaymentID]))

        self.assertEqual(response.status_code, 403)
        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.PaymentStatus, PaymentRecord.STATUS_PENDING)
        self.assertEqual(order.OrderStatus, Order.STATUS_CANCELLED)

    def test_order_with_payment_record_cannot_be_cancelled(self):
        order = Order.objects.create(CustomerName="Paid Link", Student=self.student)
        PaymentRecord.objects.create(
            Order=order,
            Amount="85.00",
            PaymentMethod="Cash",
            PaymentStatus=PaymentRecord.STATUS_PENDING,
        )

        with self.assertRaises(ValidationError):
            order.cancel()
        with self.assertRaises(ValidationError):
            order.delete()

        order.refresh_from_db()
        self.assertFalse(order.is_deleted)
        self.assertEqual(order.OrderStatus, Order.STATUS_PENDING_PAYMENT)

        self.client.force_login(self.student)
        response = self.client.post(reverse("delete_order", args=[order.OrderID]))

        self.assertRedirects(response, reverse("order_summary", args=[order.OrderID]))
        order.refresh_from_db()
        self.assertFalse(order.is_deleted)

    def test_vendor_can_view_cancelled_order_history_but_not_update_it(self):
        order = Order.objects.create(
            CustomerName="Cancelled History",
            Student=self.student,
            OrderStatus=Order.STATUS_PAYMENT_SUBMITTED,
        )
        OrderItem.objects.create(
            Order=order,
            MenuItem=self.menu_item,
            ProductName=self.menu_item.name,
            Quantity=1,
            Price=self.menu_item.price,
        )
        order.cancel()

        self.client.force_login(self.vendor)
        detail_response = self.client.get(reverse("order_summary", args=[order.OrderID]))
        update_response = self.client.post(
            reverse("update_order_status", args=[order.OrderID]),
            {"status": Order.STATUS_PROCESSING},
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "kept for history")
        self.assertEqual(update_response.status_code, 403)

    def test_vendor_cannot_create_student_order(self):
        self.client.force_login(self.vendor)

        response = self.client.post(reverse("add_new_order"), {"CustomerName": "Blocked"})

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Order.objects.filter(CustomerName="Blocked").exists())

    def test_create_order_requires_initial_item(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("add_new_order"),
            {
                "CustomerName": "No Item",
                "Quantity": 1,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertFalse(Order.objects.filter(CustomerName="No Item").exists())

    def test_deleting_last_order_item_cancels_order(self):
        order = Order.objects.create(CustomerName="Last Item", Student=self.student)
        item = OrderItem.objects.create(
            Order=order,
            MenuItem=self.menu_item,
            ProductName=self.menu_item.name,
            Quantity=1,
            Price=self.menu_item.price,
        )
        order.recompute_totals()

        self.client.force_login(self.student)
        response = self.client.get(reverse("delete_order_item", args=[order.OrderID, item.OrderItemID]))

        self.assertRedirects(response, reverse("sales_home"))
        order.refresh_from_db()
        self.assertTrue(order.is_deleted)
        self.assertEqual(order.OrderStatus, Order.STATUS_CANCELLED)
        self.assertFalse(order.items.exists())

    def test_record_payment_fails_amount_above_total_cost(self):
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
        self.assertContains(response, "Payment must cover the full order total")
        self.assertEqual(PaymentRecord.objects.filter(Order=order).count(), 0)

    def test_record_payment_fails_partial_payment(self):
        self.client.force_login(self.student)
        order = Order.objects.create(CustomerName="Partial Pay", Student=self.student)
        OrderItem.objects.create(
            Order=order,
            ProductName="Meal",
            Quantity=1,
            Price="100.00",
        )
        order.recompute_totals()

        response = self.client.post(
            reverse("record_payment", args=[order.OrderID]),
            {
                "Amount": "50.00",
                "PaymentMethod": "Cash",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Payment must cover the full order total")
        self.assertEqual(PaymentRecord.objects.filter(Order=order).count(), 0)

    def test_record_payment_fails_non_cash_payment(self):
        self.client.force_login(self.student)
        order = Order.objects.create(CustomerName="Card Pay", Student=self.student)
        OrderItem.objects.create(
            Order=order,
            ProductName="Meal",
            Quantity=1,
            Price="100.00",
        )
        order.recompute_totals()

        response = self.client.post(
            reverse("record_payment", args=[order.OrderID]),
            {
                "Amount": "100.00",
                "PaymentMethod": "Card",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice")
        self.assertEqual(PaymentRecord.objects.filter(Order=order).count(), 0)

    def test_fail_payment_sets_payment_and_order_status(self):
        order = Order.objects.create(
            CustomerName="Fail Me",
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
        response = self.client.post(reverse("fail_payment", args=[order.OrderID, payment.PaymentID]))

        self.assertRedirects(response, reverse("order_summary", args=[order.OrderID]))
        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.PaymentStatus, PaymentRecord.STATUS_FAILED)
        self.assertEqual(order.OrderStatus, Order.STATUS_PAYMENT_FAILED)
