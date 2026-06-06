"""Unit tests for the WMS module — warehouses, inventory, stock movements, shipments."""
from django.test import TestCase
from .models import Warehouse, InventoryItem, StockMovement, Shipment
from erp.models import Product


class WarehouseTests(TestCase):
    def test_str_contains_code(self):
        w = Warehouse.objects.create(name="Main Warehouse", code="WH-01")
        self.assertIn("WH-01", str(w))

    def test_is_active_default_true(self):
        w = Warehouse.objects.create(name="Secondary", code="WH-02")
        self.assertTrue(w.is_active)

    def test_code_unique_constraint(self):
        Warehouse.objects.create(name="First", code="SAME")
        with self.assertRaises(Exception):
            Warehouse.objects.create(name="Second", code="SAME")


class InventoryItemTests(TestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(name="Test WH", code="WH-T1")
        self.product = Product.objects.create(sku="INV-001", name="Test Product")

    def test_needs_reorder_when_at_or_below_level(self):
        item = InventoryItem.objects.create(
            warehouse=self.warehouse, product=self.product, quantity=5, reorder_level=10
        )
        self.assertTrue(item.needs_reorder)

    def test_no_reorder_when_above_level(self):
        item = InventoryItem.objects.create(
            warehouse=self.warehouse, product=self.product, quantity=20, reorder_level=10
        )
        self.assertFalse(item.needs_reorder)

    def test_needs_reorder_exactly_at_level(self):
        item = InventoryItem.objects.create(
            warehouse=self.warehouse, product=self.product, quantity=10, reorder_level=10
        )
        self.assertTrue(item.needs_reorder)


class StockMovementTests(TestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(name="Stock WH", code="WH-S1")
        self.product = Product.objects.create(sku="SM-001", name="Movable Item")

    def test_str_contains_direction_display(self):
        m = StockMovement.objects.create(
            warehouse=self.warehouse, product=self.product,
            direction=StockMovement.Direction.IN, quantity=50
        )
        self.assertIn("Incoming", str(m))

    def test_outgoing_direction_str(self):
        m = StockMovement.objects.create(
            warehouse=self.warehouse, product=self.product,
            direction=StockMovement.Direction.OUT, quantity=10
        )
        self.assertIn("Outgoing", str(m))


class ShipmentTests(TestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(name="Ship WH", code="WH-SH1")

    def test_default_status_is_pending(self):
        s = Shipment.objects.create(reference="SHP-001", warehouse=self.warehouse)
        self.assertEqual(s.status, Shipment.Status.PENDING)

    def test_str(self):
        s = Shipment.objects.create(reference="SHP-STR", warehouse=self.warehouse)
        self.assertEqual(str(s), "SHP-STR")
