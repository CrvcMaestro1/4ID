import os
from typing import TypeVar, Optional

_T = TypeVar("_T")


def get_env_var(key: str, default: Optional[_T] = None) -> str | _T:
    if os.getenv(key) is None and default is None:
        raise Exception(f'`{key}` environment variable is not set')
    elif os.getenv(key) is not None:
        return str(os.getenv(key))
    return str(os.getenv(key, default))
