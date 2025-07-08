import functools
from typing import Callable, TypeVar, Any, Optional
from src.app.exception.model import BaseHTTPException
from src.app.exception import ServerException
from src.app.exception.constants import ErrorTypes, ErrorTitles
import inspect

T = TypeVar('T')


def handle_exceptions(
    func: Optional[Callable[..., T]] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
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
            # Obtener el nombre de la función y el módulo para la instancia
            func_name = func.__name__
            module_name = func.__module__
            instance = f"function:{module_name}.{func_name}"

            try:
                return await func(*args, **kwargs)
            except BaseHTTPException:
                raise
            except AttributeError as e:
                raise ServerException(
                    details=f"Implementation error: {str(e)}",
                    instance=instance,
                    type_=ErrorTypes.IMPLEMENTATION_ERROR,
                    title=ErrorTitles.IMPLEMENTATION_ERROR,
                )
            except Exception as e:
                raise ServerException(
                    details=str(e),
                    instance=instance,
                    type_=ErrorTypes.SERVER_ERROR,
                    title=ErrorTitles.INTERNAL_SERVER_ERROR,
                )

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator
