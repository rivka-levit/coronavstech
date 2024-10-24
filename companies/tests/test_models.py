"""
Tests for models.
"""

import pytest


pytestmark = pytest.mark.django_db


def test_str_method_returns_company_name(amazon) -> None:
    """Test __str__ method of Company model returns company name."""

    name_expected = amazon.name
    assert str(amazon) == name_expected
