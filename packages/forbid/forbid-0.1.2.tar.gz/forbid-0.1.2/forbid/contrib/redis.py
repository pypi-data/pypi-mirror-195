from contextlib import contextmanager
from typing import Iterator

from forbid.api import forbid


@contextmanager
def forbid_redis() -> Iterator[None]:
    with forbid("redis.client.Redis.execute_command"):
        yield
