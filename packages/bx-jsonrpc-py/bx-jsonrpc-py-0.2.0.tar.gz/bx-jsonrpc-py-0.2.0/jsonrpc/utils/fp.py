from typing import Optional, TypeVar, Callable

T = TypeVar("T")
R = TypeVar("R")


def optional_map(val: Optional[T], mapper: Callable[[T], R]) -> Optional[R]:
    if val is None:
        return val
    else:
        return mapper(val)


def or_else(val: Optional[T], default: T) -> T:
    if val is None:
        return default
    else:
        return val
