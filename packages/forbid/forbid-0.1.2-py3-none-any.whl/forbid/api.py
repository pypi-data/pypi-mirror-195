from contextlib import contextmanager
from typing import Any, Callable, Iterator, NoReturn
from unittest.mock import patch

from forbid.exceptions import ForbiddenError


def _raise_for(target: str) -> Callable[..., NoReturn]:
    def _raise(*_args: Any, **_kwargs: Any) -> NoReturn:
        raise ForbiddenError(f"{target} was called")

    return _raise


@contextmanager
def forbid(target: str) -> Iterator[None]:
    with patch(target, new=_raise_for(target)):
        yield
