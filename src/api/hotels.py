from fastapi import Query, APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepositories
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location:str | None = Query(None, description = "Адрес"),
        title:str | None = Query(None, description = "Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id:int):
    async with async_session_maker() as session:
       return await HotelsRepositories(session).get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id:int):
    async with async_session_maker() as session:
        delete = await HotelsRepositories(session).delete(id = hotel_id)
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
        await session.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data:HotelAdd = Body(openapi_examples={
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
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepositories(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}

@router.put("/{hotel_id}")
async def edit_hotel(hotel_id:int, hotel_data:HotelAdd):
    async with async_session_maker() as session:
        edit = await HotelsRepositories(session).edit(hotel_data, id = hotel_id)
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
        await session.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}")
async def patch_hotel(hotel_id:int, hotel_data:HotelPatch):
    async with async_session_maker() as session:
        edit = await HotelsRepositories(session).edit(hotel_data, exclude_unset = True,  id = hotel_id)
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
        await session.commit()
    return {'status': 'OK'}
