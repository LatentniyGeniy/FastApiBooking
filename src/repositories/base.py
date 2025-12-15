from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete, exists


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)


    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalar_one()
        return self.schema.model_validate(model, from_attributes=True)


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> int:
        update_data = data.model_dump(exclude_unset=exclude_unset)
        if not update_data:
            return 0
        edit_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**update_data)
        )
        res = await self.session.execute(edit_data_stmt)
        return res.rowcount


    async def delete(self, **filter_by) -> int:
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(delete_data_stmt)
        return res.rowcount


    async def exists(self, **filters) -> bool:
        if not filters:
            raise ValueError("Необходимо указать хотя бы один фильтр")

        conditions = [getattr(self.model, key) == value for key, value in filters.items()]
        query = select(exists().where(*conditions))
        result = await self.session.execute(query)
        return result.scalar()