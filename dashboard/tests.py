"""Tests for the dashboard health endpoint."""
from django.test import TestCase
from django.urls import reverse


class HealthEndpointTests(TestCase):
    def test_health_returns_200(self):
        resp = self.client.get(reverse("dashboard:health"))
        self.assertEqual(resp.status_code, 200)

    def test_health_response_contains_ok_status(self):
        resp = self.client.get(reverse("dashboard:health"))
        self.assertEqual(resp.json()["status"], "ok")
