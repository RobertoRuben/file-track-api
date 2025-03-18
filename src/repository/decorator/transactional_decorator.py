import functools
from typing import Callable, TypeVar, Any, Optional
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.exception import DatabaseException, InvalidFieldException

T = TypeVar('T')


def transactional(func: Optional[Callable[..., T]] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to handle transactions in SQLAlchemy.
    It commits the transaction if the function is successful,
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> T:
            try:
                result = await func(self, *args, **kwargs)

                if any(method in func.__name__ for method in ['save', 'delete', 'update']):
                    await self.session.commit()

                return result

            except IntegrityError as e:
                await self.session.rollback()
                raise DatabaseException(
                    message="Error de integridad de datos",
                    details=str(e.orig),
                )
            except InvalidFieldException as e:
                raise e
            except SQLAlchemyError as e:
                await self.session.rollback()
                raise DatabaseException(
                    message=f"Error en operación de base de datos: {func.__name__}",
                    details=str(e),
                )
            except Exception as e:
                await self.session.rollback()
                raise DatabaseException(
                    message=f"Error inesperado en operación de repositorio: {func.__name__}",
                    details=str(e),
                )

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator