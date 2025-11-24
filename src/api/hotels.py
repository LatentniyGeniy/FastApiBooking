from fastapi import Query, APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location:str | None = Query(None, description = "Адрес"),
        title:str | None = Query(None, description = "Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id:int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id:int):
    delete = await db.hotels.delete(id = hotel_id)
    if delete == 0:
            raise HTTPException(
                status_code=404,
                detail="Отель не найден"
            )
    elif delete > 1:
        raise HTTPException(
            status_code=422,
            detail="Попытка удалить больше одного отеля"
        )
    await db.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(db: DBDep, hotel_data:HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель HOT 5 звезд у моря",
            "name": "sochi_u_morya",
            "location": "г.Сочи ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель R У фонтана",
            "name": "dubai_fountain",
            "location": "Дубай ул. Шейха, 2",
        }
    }
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id:int, hotel_data:HotelAdd):
    edit = await db.hotels.edit(hotel_data, id = hotel_id)
    if edit == 0:
            raise HTTPException(
                status_code=404,
                detail="Отель не найден"
            )
    elif edit > 1:
            raise HTTPException(
                status_code=422,
                detail="Попытка изменить больше одного отеля"
            )
    await db.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}")
async def patch_hotel(db: DBDep, hotel_id:int, hotel_data:HotelPatch):
    edit = await db.hotels.edit(hotel_data, exclude_unset = True,  id = hotel_id)
    if edit == 0:
        raise HTTPException(
            status_code=404,
            detail="Отель не найден"
        )
    elif edit > 1:
        raise HTTPException(
            status_code=422,
            detail="Попытка изменить больше одного отеля"
        )
    await db.commit()
    return {'status': 'OK'}
