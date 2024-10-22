"""
Tests for fibonacci endpoint
Command: pytest fib_app\tests\test_fib_api.py
"""

import pytest

from django.urls import reverse

from rest_framework import status


BASE_FIB_URL = reverse('fibonacci')


@pytest.mark.parametrize('n, expected', [(0, 0), (1, 1), (2, 1), (19, 4181)])
def test_get_with_correct_arg_success(n, expected, client) -> None:
    """Test get request with correct parameters succeeds."""

    r = client.get(f'{BASE_FIB_URL}?n={n}')

    assert r.status_code == status.HTTP_200_OK
    assert r.data['status'] == 'success'
    assert r.data['n_requested'] == n
    assert r.data['fibonacci_number'] == expected


def test_get_without_arg_fail(client) -> None:
    """Test get request without `n` parameter fails."""

    r = client.get(BASE_FIB_URL)

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data['status'] == 'error'
    assert r.data['message'] == '`n` parameter is required'


def test_get_arg_not_integer_fail(client) -> None:
    """Test get request with `n` not an integer fails."""

    wrong_arg = 'abc'
    r = client.get(f'{BASE_FIB_URL}?n={wrong_arg}')

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data['status'] == 'error'
    assert r.data['message'] == '`n` must be an integer'


def test_get_with_negative_arg_fail(client) -> None:
    """Test get request with negative `n` parameter fails."""

    wrong_arg = -15
    r = client.get(f'{BASE_FIB_URL}?n={wrong_arg}')

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data['status'] == 'error'
    assert r.data['message'] == 'Number must be positive.'


def test_post_method_not_allowed(client) -> None:
    """Test post request to fibonacci endpoint fails."""

    r = client.post(f'{BASE_FIB_URL}?n=1')

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert r.data['detail'] == 'Method "POST" not allowed.'
