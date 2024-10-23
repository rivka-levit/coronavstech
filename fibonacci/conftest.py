"""
Pytest custom fixtures for the project.
"""

import pytest
from datetime import datetime, timedelta
from collections.abc import Callable


@pytest.fixture
def time_tracker():
    tick = datetime.now()
    yield
    tock = datetime.now()
    diff = tock - tick
    print(f'\nruntime: {diff.total_seconds()} seconds')


class PerformanceException(Exception):
    def __init__(self, runtime: timedelta, limit: timedelta) -> None:
        self.runtime = runtime
        self.limit = limit

    def __str__(self):
        return (f'Performance limit exceeded, '
                f'runtime: {self.runtime}, '
                f'limit: {self.limit}')


def track_performance(
        method: Callable,
        runtime_limit: timedelta = timedelta(seconds=2)
) -> Callable:
    def run_fn_and_validate_runtime(*args, **kwargs):
        tick = datetime.now()
        result = method(*args, **kwargs)
        tock = datetime.now()
        runtime = tock - tick
        print(f'\nruntime: {runtime.total_seconds()} seconds')

        if runtime > runtime_limit:
            raise PerformanceException(runtime=runtime, limit=runtime_limit)

        return result
    return run_fn_and_validate_runtime
