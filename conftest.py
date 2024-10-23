import pytest

from companies.models import Company

from collections.abc import Callable

@pytest.fixture
def amazon() -> Company:
    return Company.objects.create(name='Amazon')


@pytest.fixture
def companies(request, company) -> list[Company]:
    companies_list = list()
    names = request.param

    for name in names:
        companies_list.append(company(name=name))

    return companies_list


@pytest.fixture
def company(**kwargs) -> Callable:
    def _company_factory(**kwargs):
        company_name = kwargs.pop('name', 'Test Company INC')
        return Company.objects.create(name=company_name, **kwargs)
    return _company_factory
