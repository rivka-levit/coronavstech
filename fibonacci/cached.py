from my_decorator import cache_fib


@cache_fib
def fibonacci_cached(n):
    if n < 0:
        raise ValueError("Fibonacci number must be greater than 0.")
    if n == 0 or n == 1:
        return n

    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)
