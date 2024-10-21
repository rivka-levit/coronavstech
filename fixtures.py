"""
Pytest custom fixtures for the project.
"""

import pytest
from datetime import datetime


@pytest.fixture
def time_tracker():
    tick = datetime.now()
    yield
    tock = datetime.now()
    diff = tock - tick
    print(f'\nruntime: {diff.total_seconds()} seconds')