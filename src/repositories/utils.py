from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel



def rooms_ids_for_bookings(
        date_from:date,
        date_to:date,
        hotel_id:int|None = None,
):
    rooms_count = (
        select(BookingsModel.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsModel)
        .filter(BookingsModel.date_from <= date_to,
                BookingsModel.date_to >= date_from,
                )
        .group_by(BookingsModel.room_id)
        .cte(name="rooms_count")
    )

    rooms_left_table = (
        select(
            RoomsModel.id.label("room_id"),
            (RoomsModel.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomsModel)
        .outerjoin(rooms_count, RoomsModel.id == rooms_count.c.room_id)
        .cte("rooms_left_table")
    )

    rooms_ids_for_hotel = (
        select(RoomsModel.id)
        .select_from(RoomsModel)
    )
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = (
        rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")
    )

    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
        )

    )
    return rooms_ids_to_get
