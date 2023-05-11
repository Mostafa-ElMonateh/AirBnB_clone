#!/usr/bin/python3
"""defines Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """represents review

    Attributes:
        place_id (str): place id
        user_id (str): user id
        text (str): text of review
    """

    place_id = ""
    user_id = ""
    text = ""
