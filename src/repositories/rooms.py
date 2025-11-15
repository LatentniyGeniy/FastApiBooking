from pydantic import BaseModel
from sqlalchemy import select, insert

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import Room, RoomAdd


class RoomsRepositories(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_all(self, hotel_id:int,):
        query = select(RoomsModel)
        query = query.where(RoomsModel.hotel_id == hotel_id)

        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]

    async def add_room(self, hotel_id:int, data: BaseModel) -> RoomAdd:
        room_data = data.model_dump()
        room_data["hotel_id"] = hotel_id
        add_data_stmt = (
            insert(self.model)
            .values(room_data)
            .returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalar_one()
        return self.schema.model_validate(model, from_attributes=True)
