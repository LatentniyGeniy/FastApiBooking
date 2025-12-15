from datetime import date

from fastapi import APIRouter, HTTPException, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example='2025-12-19'),
        date_to: date = Query(example='2025-12-21'),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id:int, room_id:int ):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id:int, room_data:RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id ,**room_data.model_dump())
    hotel = await db.hotels.exists(id=hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Отель не найден"
        )
    room = await db.rooms.add(_room_data)
    await db.session.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id:int, room_id:int):
    delete = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
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
    await db.session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id:int, room_id:int, room_data:RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id = room_id)
    await db.session.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(db: DBDep, hotel_id:int,room_id:int, room_data:RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset = True))
    await db.rooms.edit(_room_data, exclude_unset = True,  id = room_id, hotel_id=hotel_id)
    await db.session.commit()
    return {'status': 'OK'}
