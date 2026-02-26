from datetime import date

from sqlalchemy import select

from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.repositories.utils import rooms_ids_for_bookings
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


    async def get_filtered_by_time(
            self,
            location,
            title,
            limit,
            offset,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_bookings(date_from=date_from , date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsModel.hotel_id)
            .select_from(RoomsModel)
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsModel).filter(HotelsModel.id.in_(hotels_ids_to_get))
        if location:
            query = query.where(HotelsModel.location.ilike(f'%{location.strip()}%'))
        if title:
            query = query.where(HotelsModel.title.ilike(f'%{title.strip()}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


