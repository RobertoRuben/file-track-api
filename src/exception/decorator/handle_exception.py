import functools
from typing import Callable, TypeVar, Any, Optional
from src.exception.model import BaseHTTPException
from src.exception import ServerException

T = TypeVar('T')


def handle_exceptions(func: Optional[Callable[..., T]] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that handles exceptions in a unified way.
    BaseHTTPException subclasses are propagated without changes.
    Other exceptions are converted to ServerException.

    Can be used with or without parentheses:
    @handle_exceptions
    @handle_exceptions()
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return await func(*args, **kwargs)
            except BaseHTTPException:
                raise
            except AttributeError as e:
                raise ServerException(details=f"Error de implementación: {str(e)}")
            except Exception as e:
                raise ServerException(details=str(e))

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator