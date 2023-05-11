#!/usr/bin/python3
"""defines Place class"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represent a place

    Attributes:
        city_id (str): city id
        user_id (str): user id
        name (str): name of place
        description (str): description of place
        number_rooms (int): number of rooms of place
        number_bathrooms (int): number of bathrooms of place
        max_guest (int): maximum number of guests of place
        price_by_night (int): price by night of place
        latitude (float): latitude of place
        longitude (float): longitude of place
        amenity_ids (list): list of amenity ids
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
