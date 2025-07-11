import functools
from typing import Callable, TypeVar, Any, Optional, Union
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.app.core.exception import DatabaseException, InvalidFieldException

T = TypeVar('T')


def transactional(
    func: Optional[Callable[..., T]] = None, readonly: bool = False
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
            # Crear instancia para identificar dónde ocurrió el error
            instance = f"repository:{self.__class__.__module__}.{self.__class__.__name__}.{func.__name__}"

            try:
                result = await func(self, *args, **kwargs)

                if not readonly:
                    await self.session.commit()

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
                    message="Data integrity error",
                    details=str(e.orig),
                    instance=instance,
                )
            except InvalidFieldException as e:
                await self.session.rollback()
                raise e
            except AttributeError as e:
                await self.session.rollback()
                raise InvalidFieldException(
                    message="Error in provided attributes",
                    details=str(e),
                    instance=instance,
                )
            except SQLAlchemyError as e:
                await self.session.rollback()
                raise DatabaseException(
                    message=f"Error in database operation: {func.__name__}",
                    details=str(e),
                    instance=instance,
                )
            except Exception as e:
                await self.session.rollback()
                raise DatabaseException(
                    message=f"Unexpected error in repository operation: {func.__name__}",
                    details=str(e),
                    instance=instance,
                )

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator
