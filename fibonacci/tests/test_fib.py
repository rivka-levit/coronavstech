"""
Tests for fibonacci functions
Commands:
    - pytest fibonacci -v
    - pytest -v fibonacci\tests\test_fib.py
"""
import pytest

from collections.abc import Callable

from fibonacci.naive import fibonacci_naive
from fibonacci.cached import fibonacci_cached
from fibonacci.dynamic import fibonacci_dynamic
from fibonacci.dynamic import fibonacci_dynamic_v2
from conftest import time_tracker


@pytest.mark.parametrize(
    'fib_fn',
    [fibonacci_naive, fibonacci_cached, fibonacci_dynamic, fibonacci_dynamic_v2]
)
@pytest.mark.parametrize('n, expected', [(0, 0), (1, 1), (2, 1), (19, 4181)])
def test_fib(time_tracker, fib_fn: Callable, n: int, expected: int) -> None:
    res = fib_fn(n)
    assert res == expected

@pytest.mark.parametrize('fib_fn', [fibonacci_naive, fibonacci_cached])
def test_fib_naive_negative_raises_error(fib_fn: Callable) -> None:
    with pytest.raises(ValueError) as e:
        fib_fn(-5)
        assert str(e) == "Fibonacci number must be greater than 0."


@pytest.mark.parametrize('n, expected', [
    (125, 59425114757512643212875125),
    (258, 370959230771131880927453318055001997489772178180790104)])
def test_fib_cached_big_numbers(time_tracker, n: int, expected: int) -> None:
    res = fibonacci_cached(n=n)
    assert res == expected
