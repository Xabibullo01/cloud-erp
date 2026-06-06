"""Unit tests for the accounts app — User model and RBAC helpers."""
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRoleTests(TestCase):
    def test_default_role_is_sales(self):
        user = User.objects.create_user("testuser", password="pw12345!")
        self.assertEqual(user.role, User.Role.SALES)

    def test_str_contains_username_when_no_full_name(self):
        user = User.objects.create_user("alice", password="pw12345!")
        self.assertIn("alice", str(user))

    def test_is_admin_role_true_for_admin(self):
        user = User.objects.create_user("admin1", password="pw12345!", role=User.Role.ADMIN)
        self.assertTrue(user.is_admin_role)

    def test_is_admin_role_false_for_sales(self):
        user = User.objects.create_user("sales1", password="pw12345!", role=User.Role.SALES)
        self.assertFalse(user.is_admin_role)

    def test_is_manager_role_true_for_manager(self):
        user = User.objects.create_user("mgr1", password="pw12345!", role=User.Role.MANAGER)
        self.assertTrue(user.is_manager_role)

    def test_superuser_bypasses_role_check(self):
        user = User.objects.create_superuser("super1", password="pw12345!")
        self.assertTrue(user.in_roles([]))  # empty allowed list — superuser always passes
