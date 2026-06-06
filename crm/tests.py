"""Unit + integration tests for the CRM module."""
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Customer, Lead, SalesOrder, SalesOrderLine
from erp.models import Product

User = get_user_model()


class CustomerModelTests(TestCase):
    def test_total_orders_property(self):
        c = Customer.objects.create(name="Acme")
        self.assertEqual(c.total_orders, 0)
        SalesOrder.objects.create(reference="SO-1", customer=c)
        self.assertEqual(c.total_orders, 1)

    def test_customer_str(self):
        c = Customer.objects.create(name="Globex Corp")
        self.assertEqual(str(c), "Globex Corp")

    def test_customer_is_active_default(self):
        c = Customer.objects.create(name="Active Co")
        self.assertTrue(c.is_active)


class SalesOrderTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer")

    def test_order_total_sums_lines(self):
        p = Product.objects.create(sku="S1", name="Tee", unit_price=Decimal("10.00"))
        o = SalesOrder.objects.create(reference="SO-2", customer=self.customer)
        SalesOrderLine.objects.create(order=o, product=p, quantity=3, unit_price=Decimal("10.00"))
        self.assertEqual(o.total, Decimal("30.00"))

    def test_order_total_empty_is_zero(self):
        o = SalesOrder.objects.create(reference="SO-EMPTY", customer=self.customer)
        self.assertEqual(o.total, 0)

    def test_default_status_is_draft(self):
        o = SalesOrder.objects.create(reference="SO-DRAFT", customer=self.customer)
        self.assertEqual(o.status, SalesOrder.Status.DRAFT)

    def test_order_str(self):
        o = SalesOrder.objects.create(reference="SO-STR", customer=self.customer)
        self.assertEqual(str(o), "SO-STR")


class LeadTests(TestCase):
    def test_default_status_is_new(self):
        lead = Lead.objects.create(name="John Prospect")
        self.assertEqual(lead.status, Lead.Status.NEW)

    def test_str_includes_status_display(self):
        lead = Lead.objects.create(name="Jane Doe", status=Lead.Status.WON)
        self.assertIn("Won", str(lead))
        self.assertIn("Jane Doe", str(lead))


class CustomerViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u1", password="pw12345!")

    def test_list_requires_login(self):
        resp = self.client.get(reverse("crm:customer_list"))
        self.assertEqual(resp.status_code, 302)  # redirect to login

    def test_authenticated_can_create_customer(self):
        self.client.login(username="u1", password="pw12345!")
        resp = self.client.post(reverse("crm:customer_create"),
                                {"name": "New Co", "company": "X", "email": "a@b.com",
                                 "phone": "", "address": "", "is_active": "on"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Customer.objects.filter(name="New Co").exists())
