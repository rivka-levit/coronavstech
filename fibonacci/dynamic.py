def fibonacci_dynamic(n: int) -> int:
    fib_list = [0, 1]

    for i in range(1, n+1):
        fib_list.append(fib_list[i] + fib_list[i-1])

    return fib_list[n]


def fibonacci_dynamic_v2(n: int) -> int:
    if n < 0:
        raise ValueError('Number must be positive.')
    if n == 0 or n == 1:
        return n

    fib_1, fib_2 = 0, 1

    for _ in range(1, n+1):
        fib_1, fib_2 = fib_2, fib_1 + fib_2

    return fib_1