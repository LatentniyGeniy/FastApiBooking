from fastapi import Query, APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepositories
from src.repositories.rooms import RoomsRepositories
from src.schemas.rooms import Room, RoomPatch, RoomAdd

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_all(hotel_id=hotel_id)


@router.get("/rooms/{room_id}")
async def get_room(room_id:int ):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_one_or_none(id=room_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id:int, room_data:RoomAdd):
    async with async_session_maker() as session:
        hotel = await HotelsRepositories(session).exists(id=hotel_id)
        if not hotel:
            raise HTTPException(
                status_code=404,
                detail="Отель не найден"
            )

        room = await RoomsRepositories(session).add_room(hotel_id, room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete("/rooms/{room_id}")
async def delete_room(room_id:int):
    async with async_session_maker() as session:
        delete = await RoomsRepositories(session).delete(id=room_id)
        if delete == 0:
            raise HTTPException(
                status_code=404,
                detail="Номер не найден"
            )
        elif delete > 1:
            raise HTTPException(
                status_code=422,
                detail="Попытка удалить больше одного номера"
            )
        await session.commit()
    return {"status": "OK"}


@router.put("/rooms/{room_id}")
async def edit_room(room_id:int, room_data:RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(room_data, id = room_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch("/rooms/{room_id}")
async def patch_room(room_id:int, room_data:RoomPatch):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(room_data, exclude_unset = True,  id = room_id)
        await session.commit()
    return {'status': 'OK'}
