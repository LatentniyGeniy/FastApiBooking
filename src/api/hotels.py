from fastapi import  Query, APIRouter, Body

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepositories
from src.schemas.hotels import Hotel, HotelPatch
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


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id:int):
    async with async_session_maker() as session:
        await HotelsRepositories(session).delete(id = hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data:Hotel = Body(openapi_examples={
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
async def edit_hotel(hotel_id:int, hotel_data:Hotel):
    async with async_session_maker() as session:
        await HotelsRepositories(session).edit(hotel_data, id = hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id:int, hotel_data:HotelPatch):
    global hotels
    if hotel_id > 0:
        if  hotel_data.title != None and hotel_data.name != None:
            edit_hotel(hotel_id, hotel_data.title, hotel_data.name)
        elif hotel_data.title != None:
            hotels[hotel_id-1].update({'title' : hotel_data.title})
        elif hotel_data.name != None:
            hotels[hotel_id-1].update({'name' : hotel_data.name})
    else:
        return {'status': 'Bad id'}
    return {'status': 'OK'}
