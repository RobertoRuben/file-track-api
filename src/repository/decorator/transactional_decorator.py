import functools
from typing import Callable, TypeVar, Any, Optional, Union
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.exception import DatabaseException, InvalidFieldException

T = TypeVar('T')


def transactional(
        func: Optional[Callable[..., T]] = None,
        readonly: bool = False
) -> Union[Callable[..., T], Callable[[Callable[..., T]], Callable[..., T]]]:
    """
    Decorator to handle transactions in SQLAlchemy.

    Args:
        func: The function to decorate
        readonly: If True, indicates this is a read-only operation (no commit/refresh needed)
                 If False, indicates this is a write operation (needs commit/refresh)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> T:
            try:
                result = await func(self, *args, **kwargs)

                # Solo hacer commit para operaciones de escritura (readonly=False)
                if not readonly:
                    await self.session.commit()

                    # Hacer refresh después del commit
                    if result is not None:
                        if hasattr(result, '__table__'):
                            await self.session.refresh(result)
                        elif isinstance(result, list):
                            for item in result:
                                if hasattr(item, '__table__'):
                                    await self.session.refresh(item)

                return result

            except IntegrityError as e:
                await self.session.rollback()
                raise DatabaseException(
                    message="Error de integridad de datos",
                    details=str(e.orig),
                )
            except InvalidFieldException as e:
                await self.session.rollback()
                raise e
            except AttributeError as e:
                await self.session.rollback()
                raise InvalidFieldException(
                    message="Error en los atributos proporcionados",
                    details=str(e)
                )
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