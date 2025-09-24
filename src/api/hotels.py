from fastapi import  Query, APIRouter, Body

from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["hotels"])


hotels = [
    {'id' : 1, 'title' : 'Minsk', 'name': 'минск' },
    {'id' : 2,'title' : 'Kenya', 'name': 'кения' },
    {"id": 3, "title": "Sochi", "name": "sochi"},
    {"id": 4, "title": "Дубай", "name": "dubai"},
    {"id": 5, "title": "Мальдивы", "name": "maldivi"},
    {"id": 6, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 7, "title": "Москва", "name": "moscow"},
    {"id": 8, "title": "Казань", "name": "kazan"},
    {"id": 9, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id:int | None = Query(None, description = "Айди"),
        title:str | None = Query(None, description = "Название отеля"),

):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    if pagination.per_page and pagination.page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id:int):
    global hotels
    hotels = [ hotel for hotel in hotels if hotel['id'] != hotel_id ]
    return {'status': 'OK'}


@router.post("")
def create_hotel(hotel_data:Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya"
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "name": "dubai_fountain"
        }
    }
})
):
    global hotels
    hotels.append({'id' : hotels[-1]['id'] + 1, 'title' : hotel_data.title, 'name' : hotel_data.name})
    return {'status': 'OK'}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id:int, hotel_data:Hotel):
    global hotels
    if hotel_id > 0:
        hotels[hotel_id-1].update({'title' : hotel_data.title, 'name' : hotel_data.name})
    else:
        return {'status': 'Bad id'}
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
