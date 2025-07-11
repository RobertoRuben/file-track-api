import functools
from typing import Callable, TypeVar, Any, Optional
from src.app.core.exception.model import BaseHTTPException
from src.app.core.exception import ServerException
from src.app.core.exception.constants import ErrorTypes, ErrorTitles

T = TypeVar('T')


def service_handle_exceptions(
    func: Optional[Callable[..., T]] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator que unifica el manejo de excepciones:
    - Propaga sin cambiar las BaseHTTPException.
    - Convierte otras exceptions en ServerException.
    Permite usarse con o sin paréntesis.
    """

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            # Buscamos un objeto Request en args/kwargs para extraer la ruta
            request = None
            for arg in list(args) + list(kwargs.values()):
                if hasattr(arg, 'url') and hasattr(arg, 'method'):
                    request = arg
                    break

            instance = (
                request.url.path
                if request is not None
                else f"urn:problem-instance:{fn.__name__}"
            )

            try:
                return await fn(*args, **kwargs)

            except BaseHTTPException:
                # 1) Propagamos la excepción original sin modificarla
                raise

            except AttributeError as e:
                # errores de implementación (atributo faltante, etc.)
                raise ServerException(
                    details=f"Implementation error: {e}",
                    instance=instance,
                    type_=ErrorTypes.IMPLEMENTATION_ERROR,
                    title=ErrorTitles.IMPLEMENTATION_ERROR,
                )

            except Exception as e:
                # cualquier otro error en el servicio
                raise ServerException(
                    details=str(e),
                    instance=instance,
                    type_=ErrorTypes.SERVER_ERROR,
                    title=ErrorTitles.INTERNAL_SERVER_ERROR,
                )

        return wrapper

    # Permite usar @handle_exceptions o @handle_exceptions()
    if func:
        return decorator(func)  # decoramos directamente

    return decorator
