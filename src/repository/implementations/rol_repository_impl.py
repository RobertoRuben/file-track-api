import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.repository.decorator import transactional
from src.repository.interfaces import IRolRepository
from src.model.entity import Rol
from src.exception import InvalidFieldException
from src.schema import Page, Pagination


class RolRepositoryImpl(IRolRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    @transactional(readonly=False)
    async def save(self, rol: Rol) -> Rol:
        self.session.add(rol)
        # El refresh lo hace automáticamente el decorador
        return rol

    @transactional(readonly=True)
    async def get_all(self) -> list[Rol]:
        stmt = select(Rol)
        results = await self.session.exec(stmt)
        roles = results.all()
        return list(roles)

    @transactional(readonly=False)
    async def delete(self, rol_id: int) -> bool:
        rol = await self.get_by_id(rol_id)
        await self.session.delete(rol)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, rol_id: int) -> Rol:
        stmt = select(Rol).where(Rol.id == rol_id)
        results = await self.session.exec(stmt)
        rol = results.first()
        return rol

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        offset_value = (page - 1) * size
        stmt = select(Rol)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        roles = list(results.all())

        count_stmt = select(func.count(Rol.id))
        count_results = await self.session.exec(count_stmt)
        total_items = count_results.first()
        total_pages = math.ceil(total_items / size) if total_items > 0 else 1

        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        page_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page
        )

        return Page(
            data=roles,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["nombre"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "nombre":
                normalized_search = search_value.lower()
                conditions.append(func.lower(Rol.nombre).like(f"%{normalized_search}%"))

        stmt = select(Rol)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        roles = list(results.all())

        count_stmt = select(func.count(Rol.id))

        if conditions:
            count_stmt = count_stmt.where(or_(*conditions))

        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()

        total_pages = math.ceil(total_items / size) if total_items > 0 else 1
        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        page_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(
            data=roles,
            meta=page_info
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        valid_fields = Rol.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Rol model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}"
                )

        stmt = select(Rol.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Rol, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None