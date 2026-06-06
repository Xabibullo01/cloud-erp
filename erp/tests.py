"""Unit tests for the ERP module — products, categories, suppliers, purchase orders."""
from django.test import TestCase
from .models import Category, Product, Supplier, Employee, PurchaseOrder


class CategoryTests(TestCase):
    def test_str(self):
        cat = Category.objects.create(name="Electronics")
        self.assertEqual(str(cat), "Electronics")

    def test_unique_name_constraint(self):
        Category.objects.create(name="Unique")
        with self.assertRaises(Exception):
            Category.objects.create(name="Unique")


class ProductTests(TestCase):
    def test_str_includes_sku_and_name(self):
        p = Product.objects.create(sku="SKU-001", name="Widget")
        self.assertIn("SKU-001", str(p))
        self.assertIn("Widget", str(p))

    def test_is_active_default_true(self):
        p = Product.objects.create(sku="SKU-002", name="Gadget")
        self.assertTrue(p.is_active)

    def test_unique_sku_constraint(self):
        Product.objects.create(sku="DUPE", name="First")
        with self.assertRaises(Exception):
            Product.objects.create(sku="DUPE", name="Second")

    def test_product_with_category(self):
        cat = Category.objects.create(name="Tools")
        p = Product.objects.create(sku="SKU-CAT", name="Hammer", category=cat)
        self.assertEqual(p.category, cat)


class SupplierTests(TestCase):
    def test_str(self):
        s = Supplier.objects.create(name="Acme Corp")
        self.assertEqual(str(s), "Acme Corp")


class PurchaseOrderTests(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(name="Supplier X")

    def test_default_status_is_draft(self):
        po = PurchaseOrder.objects.create(reference="PO-001", supplier=self.supplier)
        self.assertEqual(po.status, PurchaseOrder.Status.DRAFT)

    def test_str(self):
        po = PurchaseOrder.objects.create(reference="PO-STR", supplier=self.supplier)
        self.assertEqual(str(po), "PO-STR")
