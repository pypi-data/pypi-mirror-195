from collections.abc import Callable
from functools import reduce
from typing import Any, TypeGuard, TypeVar, get_args, get_origin, is_typeddict

T = TypeVar("T")


def autocast(data: Any, t: type[T]) -> T:
    if autoguard(t)(data):
        return data
    else:
        raise TypeError(f"{data} is not of type {t}")


def autoguard(t: type[T]) -> Callable[[Any], TypeGuard[T]]:
    if is_typeddict(t):
        keys = t.__annotations__.keys()
        kg = autoguard(dict[str, Any])
        vgs = {k: autoguard(v) for k, v in t.__annotations__.items()}

        def inner(data: Any) -> TypeGuard[T]:
            return (
                kg(data)
                and set(data.keys()) == set(keys)
                and reduce(lambda acc, x: acc and vgs[x](data[x]), keys, True)
            )

    elif get_origin(t) is dict:
        kt, vt = get_args(t)
        kg = autoguard(kt)
        vg = autoguard(vt)

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, dict) and all(kg(x) for x in data.keys()) and all(vg(x) for x in data.values())

    elif get_origin(t) is list:
        vt = get_args(t)[0]
        vg = autoguard(vt)

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, list) and all(vg(x) for x in data)

    elif get_origin(t) is set:
        vt = get_args(t)[0]
        vg = autoguard(vt)

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, set) and all(vg(x) for x in data)

    elif get_origin(t) is tuple:
        vgs2 = [autoguard(x) for x in get_args(t)]

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, tuple) and len(data) == len(vgs2) and all(vg(x) for vg, x in zip(vgs2, data))

    elif get_origin(t) is type:
        vt = get_args(t)[0]

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, type) and data == vt

    elif t is Any:

        def inner(data: Any) -> TypeGuard[T]:
            return True

    else:

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, t)

    return inner
