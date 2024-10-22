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


@pytest.mark.parametrize(
    argnames='n, msg',
    argvalues=[
        ('abc', '`n` must be an integer'),
        (3.5, '`n` must be an integer'),
        (-15, 'Number must be positive.')
    ]
)
def test_fib_api_with_wrong_argument_fails(
        client: pytest.fixture,
        n: str | int | float,
        msg: str) -> None:
    """Test get request with wrong argument fails."""

    r = client.get(f'{BASE_FIB_URL}?n={n}')

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data['status'] == 'error'
    assert r.data['message'] == msg



def test_post_method_not_allowed(client) -> None:
    """Test post request to fibonacci endpoint fails."""

    r = client.post(f'{BASE_FIB_URL}?n=1')

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert r.data['detail'] == 'Method "POST" not allowed.'


@pytest.mark.parametrize(
    argnames='n, expected',
    argvalues=[
        (125, 59425114757512643212875125),
        (258, 370959230771131880927453318055001997489772178180790104),
        (1000, 43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875)
    ]
)
def test_stress_big_numbers_success(client, n: int, expected: int) -> None:
    """Stress test to assure that fib endpoint works with big numbers."""

    r = client.get(f'{BASE_FIB_URL}?n={n}')

    assert r.status_code == status.HTTP_200_OK
    assert r.data['status'] == 'success'
    assert r.data['n_requested'] == n
    assert r.data['fibonacci_number'] == expected
