"""
Testing API with the Requests library. Django agnostic tests.
Needs no parallel workers in pytest.ini

Command to run tests:   --> pytest companies\tests\test_generic_api.py
Command to clean up db: --> python manage.py flush --no-input
"""

import pytest
import requests
import responses
import json
import os

from dotenv import load_dotenv

load_dotenv()


COMPANIES_LIST = 'http://127.0.0.1:8000/companies/'


def cleanup_company(company_id: str) -> None:
    """Delete a company from the database."""

    r = requests.delete(url=f'{COMPANIES_LIST}{company_id}/')
    assert r.status_code == 204


@pytest.mark.skip_in_ci
@pytest.mark.skip(reason='Test needs host django server running')
def test_zero_companies_django_agnostic() -> None:
    """
    Test GET request returns empty list if there are no companies
    in the database.
    """

    r = requests.get(url=COMPANIES_LIST)

    assert r.status_code == 200
    assert json.loads(r.content) == []


@pytest.mark.skip_in_ci
@pytest.mark.skip(reason='Test needs host django server running')
def test_create_company_with_layoffs_django_agnostic() -> None:
    """Test creating a company with layoffs status succeeds."""

    payload = {'name': 'test company name', 'status': 'Layoffs'}
    r = requests.post(url=COMPANIES_LIST, data=payload)
    r_content = json.loads(r.content)

    assert r.status_code == 201
    assert r_content['name'] == payload['name']
    assert r_content['status'] == payload['status']

    cleanup_company(company_id=r_content['id'])


@pytest.mark.change
def test_exchangerate_api() -> None:
    """Test exchangerate API call."""

    cur1 = 'USD'
    cur2 = 'ILS'
    amount = 100
    base_url = 'https://api.exchangerate.host/convert'
    key = os.environ.get('ACCESS_KEY')

    r = requests.get(
        url=f'{base_url}?from={cur1}&to={cur2}&amount={amount}&access_key={key}'
    )
    response_json = r.json()
    assert r.status_code == 200
    assert 'query' in response_json
    assert 'result' in response_json
    assert response_json['query']['from'] == cur1
    assert response_json['query']['to'] == cur2


@pytest.mark.change
@responses.activate
def test_mocked_exchangerate_api() -> None:

    cur1 = 'BLA'
    cur2 = 'CLA'
    amount = 100
    base_url = 'https://api.exchangerate.host/convert'
    key = os.environ.get('ACCESS_KEY')

    responses.add(
        responses.GET,
        f'{base_url}?from={cur1}&to={cur2}&amount={amount}&access_key={key}',
        json={"success":'true',
              "query":{"from":f"{cur1}","to":f"{cur2}","amount":100},
              "quote":3.8,
              "result":380.0},
        status=200,
    )

    assert process_exchange() == 29


def process_exchange():
    cur1 = 'BLA'
    cur2 = 'CLA'
    amount = 100
    base_url = 'https://api.exchangerate.host/convert'
    key = os.environ.get('ACCESS_KEY')

    r = requests.get(
        url=f'{base_url}?from={cur1}&to={cur2}&amount={amount}&access_key={key}'
    )
    response_json = r.json()

    if r.status_code != 200:
        raise ValueError('Request failed')

    from_cur = response_json['query']['from']
    to_cur = response_json['query']['to']
    if from_cur == cur1 and to_cur == cur2:
        # The response was mocked
        return 29

    return 42
