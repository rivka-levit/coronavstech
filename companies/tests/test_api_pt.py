"""
Tests for Company app API in pytest style
Commands:
    - pytest -v
    - pytest -v -s (to see what was printed out)
    - pytest -v --durations=0 -vv (to see the duration of every test)
    - pytest -k [part_name_of_test_function] (to run selected tests)
"""
import pytest

from django.urls import reverse

from rest_framework import status

from companies.models import Company


COMPANIES_LIST = reverse('companies-list')
pytestmark = pytest.mark.django_db  # decorator for all the functions in the file

# ------------------- Test Get Companies ---------------------

def test_zero_companies_should_return_empty_list(client) -> None:
    """
    Test GET request returns empty list if there are no companies
    in the database.
    """

    r = client.get(COMPANIES_LIST)

    assert r.status_code == status.HTTP_200_OK
    assert r.data == []


def test_one_company_exists_should_succeed(client) -> None:
    """Test GET request returns one company if one company exists."""

    amazon = Company.objects.create(name='Amazon')
    r = client.get(COMPANIES_LIST)

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 1
    assert r.data[0]['name'] == amazon.name
    assert r.data[0]['status'] == amazon.status
    assert r.data[0]['app_link'] == amazon.app_link
    assert r.data[0]['notes'] == amazon.notes

# ------------------- Test Post Companies ---------------------

def test_create_company_without_arguments_fails(client) -> None:
    """Test creating a company with no arguments fails."""

    payload = {}
    r = client.post(COMPANIES_LIST, data=payload)

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data['name'] == ['This field is required.']


def test_create_existing_company_fails(client) -> None:
    """Test creating a company with an existing name fails."""

    Company.objects.create(name='Amazon')
    payload = {'name': 'Amazon'}
    r = client.post(COMPANIES_LIST, data=payload)

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data['name'] == ['company with this name already exists.']


def test_create_company_with_name_set_default_fields(client) -> None:
    """
    Test creating a company with only name successful and set default
    fields for the rest of data.
    """

    payload = {'name': 'test company name'}
    expected_default = {
        'status': 'Hiring',
        'app_link': '',
        'notes': '',
    }

    r = client.post(COMPANIES_LIST, data=payload)

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data['name'] == payload['name']
    assert r.data['status'] == expected_default['status']
    assert r.data['app_link'] == expected_default['app_link']
    assert r.data['notes'] == expected_default['notes']


def test_create_company_with_layoffs_status_success(client) -> None:
    """Test creating a company with layoffs status succeeds."""

    payload = {'name': 'test company name', 'status': 'Layoffs'}
    r = client.post(COMPANIES_LIST, data=payload)

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data['name'] == payload['name']
    assert r.data['status'] == payload['status']


def test_create_company_with_wrong_status_fails(client) -> None:
    """Test creating a company with a wrong status fails."""

    payload = {'name': 'test company name', 'status': 'Wrong'}
    r = client.post(COMPANIES_LIST, data=payload)

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert 'is not a valid choice' in str(r.content)
    # assert r.data['status'] == [f'"{payload['status']}" is not a valid choice.']
