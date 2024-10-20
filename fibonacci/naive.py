def fibonacci_naive(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci number must be greater than 0.")
    if n == 0 or n == 1:
        return n

    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


print(fibonacci_naive(7))
