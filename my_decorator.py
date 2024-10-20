import re
from typing import Any, Callable


def get_list_of_kwargs_for_function(
        identifiers: str,
        values: list[tuple[int, int]]
) -> list[dict[str, Any]]:
    parsed_identifiers = re.split(r', |,', identifiers)
    kwargs_for_run_fn = list()
    for tpl_values in values:
        kwg_item = dict()
        for i, keyword in enumerate(parsed_identifiers):
            kwg_item[keyword] = tpl_values[i]
        kwargs_for_run_fn.append(kwg_item)
    return kwargs_for_run_fn


def my_parametrize(
        identifiers: str,
        values: list[tuple[int, int]]
) -> Callable:

    def decorator(fn: Callable) -> Callable:

        def wrapper() -> None:
            kwargs_for_run_fn = get_list_of_kwargs_for_function(identifiers, values)

            for ks in kwargs_for_run_fn:
                print(f'calling {fn.__name__} with {ks}')
                fn(**ks)

        return wrapper
    return decorator
