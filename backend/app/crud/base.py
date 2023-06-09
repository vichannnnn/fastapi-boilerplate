from typing import TypeVar, Generic

from sqlalchemy import update, delete, select
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm.decl_api import DeclarativeMeta

from app.db.base_class import Base
from app.api.deps import CurrentSession


ModelType = TypeVar("ModelType")


class CRUD(Generic[ModelType]):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__class__.__name__.lower()

    @classmethod
    async def create(
        cls: DeclarativeMeta, session: CurrentSession, data: dict
    ) -> ModelType:
        obj = cls(**data)
        session.add(obj)
        await session.commit()
        return obj

    @classmethod
    async def get(cls: Base, session: CurrentSession, id: int) -> ModelType:
        stmt = select(cls).where(cls.id == id)
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def update(
        cls: Base, session: CurrentSession, id: int, data: dict
    ) -> ModelType:
        stmt = update(cls).returning(cls).where(cls.id == id).values(**data)
        res = await session.execute(stmt)
        await session.commit()
        updated_obj = res.scalar()
        return updated_obj

    @classmethod
    async def delete(cls: Base, session: CurrentSession, id: int) -> ModelType:
        stmt = delete(cls).where(cls.id == id)
        fetch_stmt = select(cls).where(cls.id == id)

        res = await session.execute(fetch_stmt)
        await session.execute(stmt)
        deleted_obj = res.scalar()
        await session.commit()
        return deleted_obj

    @classmethod
    async def get_all(cls: Base, session: CurrentSession):
        stmt = select(cls)
        result = await session.execute(stmt)
        return result.scalars().all()
