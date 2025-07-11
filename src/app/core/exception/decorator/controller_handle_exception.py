import functools
from fastapi import Request
from typing import Callable, TypeVar, Any
from src.app.core.exception.model import BaseHTTPException
from src.app.core.exception import ServerException
from src.app.core.exception.constants import ErrorTypes, ErrorTitles

T = TypeVar('T')


def controller_handle_exceptions(func: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        request: Request = kwargs.get('request', None)
        if request is None:
            # Buscar en los args
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        instance = (
            request.url.path if request else f"urn:problem-instance:{func.__name__}"
        )
        try:
            return await func(*args, **kwargs)
        except BaseHTTPException as e:
            if hasattr(e, 'detail') and isinstance(e.detail, dict):
                if e.detail.get('instance') is None:
                    e.detail['instance'] = instance
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
