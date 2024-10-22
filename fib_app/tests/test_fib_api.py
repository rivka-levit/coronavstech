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
    r = client.get(f'{BASE_FIB_URL}?n={n}')

    assert r.status_code == status.HTTP_200_OK
    assert r.data['n_requested'] == n
    assert r.data['fibonacci_number'] == expected
