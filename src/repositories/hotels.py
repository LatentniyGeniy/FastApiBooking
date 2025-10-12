from sqlalchemy import select


from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel


class HotelsRepositories(BaseRepository):
    model = HotelsModel
    schema = Hotel

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

            return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]