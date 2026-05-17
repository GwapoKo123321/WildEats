from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class RoleRegistrationTests(TestCase):
    def register_user(self, role, username):
        return self.client.post(
            f"{reverse('register')}?role={role}",
            {
                "role": role,
                "first_name": username.title(),
                "last_name": "User",
                "username": username,
                "email": f"{username}@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

    def test_register_page_shows_role_picker_without_query_string(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Who are you registering as?")
        self.assertContains(response, "?role=student")

    def test_student_registration_creates_student_user_only(self):
        response = self.register_user("student", "studentuser")

        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="studentuser")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.groups.filter(name="student").exists())
        self.assertFalse(user.groups.filter(name="vendor").exists())
        self.assertFalse(user.groups.filter(name="admin").exists())

    def test_registration_rejects_duplicate_username(self):
        User.objects.create_user(username="Juan", password="StrongPass123!")

        response = self.register_user("student", "Juan")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already exists")
        self.assertEqual(User.objects.filter(username="Juan").count(), 1)

    def test_registration_rejects_duplicate_username_with_different_case(self):
        User.objects.create_user(username="Juan", password="StrongPass123!")

        response = self.register_user("student", "juan")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already exists")
        self.assertFalse(
            User.objects.exclude(username="Juan").filter(username__iexact="juan").exists()
        )

    def test_vendor_registration_creates_staff_user(self):
        response = self.register_user("vendor", "vendoruser")

        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="vendoruser")
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.groups.filter(name="vendor").exists())
        self.assertFalse(user.groups.filter(name="student").exists())
        self.assertFalse(user.groups.filter(name="admin").exists())

    def test_registered_vendor_can_log_in_to_vendor_dashboard(self):
        self.register_user("vendor", "newvendor")

        login_response = self.client.post(reverse("login"), {
            "username": "newvendor",
            "password": "StrongPass123!",
        })
        dashboard = self.client.get(login_response["Location"])

        self.assertRedirects(login_response, reverse("sales_home"))
        self.assertContains(dashboard, "Vendor Dashboard")

    def test_admin_registration_creates_superuser(self):
        response = self.register_user("admin", "adminuser")

        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="adminuser")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.groups.filter(name="admin").exists())

    def test_role_dashboards_after_login(self):
        student_group = Group.objects.create(name="student")
        vendor_group = Group.objects.create(name="vendor")
        admin_group = Group.objects.create(name="admin")

        student = User.objects.create_user(username="student", password="StrongPass123!")
        vendor = User.objects.create_user(username="vendor", password="StrongPass123!", is_staff=True)
        admin = User.objects.create_user(
            username="admin",
            password="StrongPass123!",
            is_staff=True,
            is_superuser=True,
        )
        student.groups.add(student_group)
        vendor.groups.add(vendor_group)
        admin.groups.add(admin_group)

        self.client.login(username="student", password="StrongPass123!")
        self.assertContains(self.client.get(reverse("sales_home")), "Student Dashboard")

        self.client.logout()
        self.client.login(username="vendor", password="StrongPass123!")
        self.assertContains(self.client.get(reverse("sales_home")), "Vendor Dashboard")

        self.client.logout()
        self.client.login(username="admin", password="StrongPass123!")
        self.assertContains(self.client.get(reverse("sales_home")), "Admin Dashboard")

    def test_login_repairs_existing_role_flags(self):
        vendor_group = Group.objects.create(name="vendor")
        admin_group = Group.objects.create(name="admin")
        student_group = Group.objects.create(name="student")
        vendor = User.objects.create_user(username="oldvendor", password="StrongPass123!")
        admin = User.objects.create_user(username="oldadmin", password="StrongPass123!")
        student = User.objects.create_user(username="oldstudent", password="StrongPass123!", is_staff=True)
        conflicted_student = User.objects.create_user(
            username="conflictedstudent",
            password="StrongPass123!",
            is_staff=True,
        )
        vendor.groups.add(vendor_group)
        admin.groups.add(admin_group)
        student.groups.add(student_group)
        conflicted_student.groups.add(student_group, vendor_group)

        self.client.post(reverse("login"), {
            "username": "oldvendor",
            "password": "StrongPass123!",
        })
        vendor.refresh_from_db()
        self.assertTrue(vendor.is_staff)
        self.assertFalse(vendor.is_superuser)

        self.client.logout()
        self.client.post(reverse("login"), {
            "username": "oldadmin",
            "password": "StrongPass123!",
        })
        admin.refresh_from_db()
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

        self.client.logout()
        self.client.post(reverse("login"), {
            "username": "oldstudent",
            "password": "StrongPass123!",
        })
        student.refresh_from_db()
        self.assertFalse(student.is_staff)
        self.assertFalse(student.is_superuser)

        self.client.logout()
        self.client.post(reverse("login"), {
            "username": "conflictedstudent",
            "password": "StrongPass123!",
        })
        conflicted_student.refresh_from_db()
        self.assertFalse(conflicted_student.is_staff)
        self.assertFalse(conflicted_student.is_superuser)
        self.assertTrue(conflicted_student.groups.filter(name="student").exists())
        self.assertFalse(conflicted_student.groups.filter(name="vendor").exists())
