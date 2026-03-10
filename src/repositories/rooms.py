from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.repositories.utils import rooms_ids_for_bookings
from src.schemas.rooms import Room, RoomsWithRels


class RoomsRepositories(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from:date,
            date_to:date
    ):
        rooms_ids_to_get = rooms_ids_for_bookings(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [RoomsWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]



    async def get_one_or_none_with_rels(self, **filter_by):
        query = (select(self.model)
                 .options(selectinload(self.model.facilities))
                 .filter_by(**filter_by)
                 )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomsWithRels.model_validate(model, from_attributes=True)