"""
Tests for Company app API
Commands:
    - pytest -v
    - pytest -v -s (to see what was printed out)
"""

import json
# import pytest

from django.test import Client, TestCase
from django.urls import reverse

from rest_framework import status

from companies.models import Company


# @pytest.mark.django_db
class TestGetCompanies(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('companies-list')

    def test_zero_companies_should_return_empty_list(self) -> None:
        """
        Test GET request returns empty list if there are no companies
        in the database.
        """

        r = self.client.get(self.list_url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(r.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        """Test GET request returns one company if one company exists."""

        amazon = Company.objects.create(name='Amazon')
        r = self.client.get(self.list_url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]['name'], amazon.name)
        self.assertEqual(r.data[0]['status'], amazon.status)
        self.assertEqual(r.data[0]['app_link'], amazon.app_link)
        self.assertEqual(r.data[0]['notes'], amazon.notes)
