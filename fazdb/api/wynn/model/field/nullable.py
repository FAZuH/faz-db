from typing import Any


class Nullable:
    """Any object that's wrapped by `Nullable` will return `None` if the class argument is only `None`."""

    def __new__[T](cls, class_: type[T], *args, **kwargs: Any) -> None | T:
        if len(args) == 1 and args[0] is None:
            return None
        return class_(*args, **kwargs)
