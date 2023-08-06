from contextlib import contextmanager
from typing import Iterator

from forbid.api import forbid


@contextmanager
def forbid_requests() -> Iterator[None]:
    with forbid("requests.sessions.Session.request"):
        yield
