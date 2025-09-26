
from sqlalchemy import insert, select

from app.database import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id:int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_all(cls):
        async with async_session() as session:
            query = select(cls.model)
            res = await session.execute(query)
            return res.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_by_another_id(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            res = await session.execute(query)
            return res.scalars().all()