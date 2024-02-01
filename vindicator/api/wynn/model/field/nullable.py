from typing import Any, TypeVar

T = TypeVar('T')


class Nullable:
    """Any object that's wrapped by `Nullable` will return `None` if the class argument is only `None`."""

    def __new__(cls, class_: type[T], *args: Any, **kwargs: Any) -> None | T:
        if len(args) == 1 and args[0] is None:
            return None
        return class_(*args, **kwargs)
