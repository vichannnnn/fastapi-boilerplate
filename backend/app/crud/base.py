from typing import TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr
from sqlalchemy import update, delete, select

ModelType = TypeVar("ModelType")


class CRUD(Generic[ModelType]):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> ModelType:
        obj = cls(**data)
        session.add(obj)
        await session.commit()
        return obj

    @classmethod
    async def read(cls, session: AsyncSession, id: int) -> ModelType:
        stmt = select(cls).where(cls.id == id)
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def update(cls, session: AsyncSession, id: int, data: dict) -> ModelType:
        stmt = update(cls).returning(cls).where(cls.id == id).values(**data)
        res = await session.execute(stmt)
        await session.commit()
        updated_object = res.fetchone()
        return updated_object

    @classmethod
    async def delete(cls, session: AsyncSession, id: int) -> ModelType:
        stmt = delete(cls).returning(cls).where(cls.id == id)
        res = await session.execute(stmt)
        await session.commit()
        deleted_object = res.fetchone()
        return deleted_object

    @classmethod
    async def get_all(cls, session: AsyncSession):
        stmt = select(cls)
        result = await session.execute(stmt)
        return result.scalars().all()
