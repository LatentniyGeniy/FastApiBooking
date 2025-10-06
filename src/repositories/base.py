from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        return result.scalar_one()

    async def edit(self, data: BaseModel, **filter_by) -> int:
        update_data = data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
        if not update_data:
            return 0
        edit_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**update_data)
        )
        res = await self.session.execute(edit_data_stmt)
        return res.rowcount


    async def delete(self, **filter_by):
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(delete_data_stmt)
        return res.rowcount