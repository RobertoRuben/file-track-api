from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.db.dependencies import get_async_session
from src.app.repository.interfaces import ICategoriaDocumentoRepository
from src.app.repository.implementations import CategoriaRepositoryImpl

async def get_categoria_documento_repository(session: AsyncSession = Depends(get_async_session)) -> ICategoriaDocumentoRepository:
    """
    Dependency function to get the document category repository implementation.

    Args:
        session: The async database session provided by the FastAPI dependency injection system

    Returns:
        An implementation of ICategoriaDocumentoRepository bound to the provided session
    """
    return CategoriaRepositoryImpl(session=session)