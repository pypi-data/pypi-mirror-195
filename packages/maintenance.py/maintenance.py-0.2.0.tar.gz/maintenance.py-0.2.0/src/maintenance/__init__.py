from collections.abc import Callable
from functools import wraps
from textwrap import fill
from typing import Any, NoReturn, Optional, overload, ParamSpec, TypeVar
from warnings import warn

P = ParamSpec("P")
R = TypeVar("R")


class UnstableWarning(UserWarning):
    """
    Warning for unstable features.
    """

@overload
def todo(fn: None = None) -> NoReturn: ...

@overload
def todo(fn: Callable[P, R]) -> Callable[P, R]: ...

def todo(fn: Optional[Callable[P, R]] = None) -> Callable[P, NoReturn] | NoReturn:
    if fn is None:
        raise NotImplementedError("TODO")

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> NoReturn:
        todo()
    
    return wrapper

def deprecated(
    message: Optional[str] = None,
    *,
    since: Optional[str] = None,
    new: Any = None,
    add_sphinx_directive: bool = False
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Parameters
    ----------
    message
        Overrides the default warn message.
    
    since
        The version since when the object is deprecated.

    new
        The new object that replaces the deprecated one. This may be
        the object itself or its name as a string.

    add_sphinx_directive
        Adds the
        [deprecated directive](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-deprecated)
        to the beginning of the docstring of the object.

    Examples
    --------
    ```python
    def new():
        return 1

    @deprecated(since="1.2.3.post4", new=new)
    def old():
        return None
    ```
    """
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        doc = f"\n.. deprecated:: {since}\n"
        if message is not None:
            doc += fill(message, initial_indent=" " * 3, subsequent_indent=" " * 3) + "\n"
        
        fn.__doc__ = doc + (fn.__doc__ or "")
        
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            warn(
                message or (
                    "Using this object is deprecated"
                    + (f" since version {since}" if since else "")
                    + (f"; use {new!r} instead" if new is not None else "")
                    + "."
                ),
                DeprecationWarning
            )
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def unstable(
    message: Optional[str] = None,
    *,
    until: Optional[str] = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            warn(
                message or (
                    "This feature is unstable"
                    + (f" and is expected to be stable in version {until}" if until else "")
                    + "."
                ),
                UnstableWarning
            )
            return fn(*args, **kwargs)
        return wrapper
    return decorator
