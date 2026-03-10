from pydantic import BaseModel
from sqlalchemy import update, select, delete
from sqlalchemy.dialects.mysql import insert

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepositories(BaseRepository):
    model = FacilitiesModel
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    schema = RoomFacility


    async def set_rooms_facilities(self, room_id: int, facilities_ids: list[int]) -> int:
        query = select(self.model.facility_id).filter_by(room_id = room_id)
        res = await self.session.execute(query)
        current_facilities_ids: list[int] = res.scalars().all()

        ids_to_del: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_ins: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_del:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_del),
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_ins:
            ins_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_ins])
            )
            await self.session.execute(ins_m2m_facilities_stmt)

        return res.rowcount