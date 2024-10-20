"""
Tests for fibonacci functions
Commands:
    - pytest fibonacci -v
    - pytest -v fibonacci\tests\test_fib.py
"""
import pytest

from fibonacci.naive import fibonacci_naive


@pytest.mark.parametrize('n, expected', [(0, 0), (1, 1), (2, 1), (7, 13)])
def test_fib_naive(n: int, expected: int) -> None:
    res = fibonacci_naive(n=n)
    assert res == expected


def test_fib_naive_negative_raises_error() -> None:
    with pytest.raises(ValueError) as e:
        fibonacci_naive(-5)
        assert str(e) == "Fibonacci number must be greater than 0."
