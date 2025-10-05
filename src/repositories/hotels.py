from sqlalchemy import select, insert

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel


class HotelsRepositories(BaseRepository):
    model = HotelsModel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
        ):
            query = select(HotelsModel)
            if location:
                query = query.where(HotelsModel.location.ilike(f'%{location.strip()}%'))
            if title:
                query = query.where(HotelsModel.title.ilike(f'%{title.strip()}%'))
            query = (
                query
                .limit(limit)
                .offset(offset)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(query)

            return result.scalars().all()


    async def add(self, hotel_data):
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        await self.session.execute(add_hotel_stmt)
