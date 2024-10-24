"""
Testing API with the Requests library. Django agnostic tests.
Needs no parallel workers in pytest.ini

Command to run tests:   --> pytest companies\tests\test_generic_api.py
Command to clean up db: --> python manage.py flush --no-input
"""

import pytest
import requests
import json


COMPANIES_LIST = 'http://127.0.0.1:8000/companies/'


def cleanup_company(company_id: str) -> None:
    """Delete a company from the database."""

    r = requests.delete(url=f'{COMPANIES_LIST}{company_id}/')
    assert r.status_code == 204


@pytest.mark.skip_in_ci
def test_zero_companies_django_agnostic() -> None:
    """
    Test GET request returns empty list if there are no companies
    in the database.
    """

    r = requests.get(url=COMPANIES_LIST)

    assert r.status_code == 200
    assert json.loads(r.content) == []


@pytest.mark.skip_in_ci
def test_create_company_with_layoffs_django_agnostic() -> None:
    """Test creating a company with layoffs status succeeds."""

    payload = {'name': 'test company name', 'status': 'Layoffs'}
    r = requests.post(url=COMPANIES_LIST, data=payload)
    r_content = json.loads(r.content)

    assert r.status_code == 201
    assert r_content['name'] == payload['name']
    assert r_content['status'] == payload['status']

    cleanup_company(company_id=r_content['id'])
