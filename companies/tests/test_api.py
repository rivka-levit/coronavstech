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
class BasicCompanyAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('companies-list')

    def tearDown(self):
        pass


class TestGetCompanies(BasicCompanyAPITestCase):
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


class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_fails(self) -> None:
        """Test creating a company with no arguments fails."""

        payload = {}
        r = self.client.post(self.list_url, data=payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.data['name'], ['This field is required.'])

    def test_create_existing_company_fails(self) -> None:
        """Test creating a company with an existing name fails."""

        Company.objects.create(name='Amazon')
        payload = {'name': 'Amazon'}
        r = self.client.post(self.list_url, data=payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.data['name'],
            ['company with this name already exists.']
        )
