#!/usr/bin/python3
"""defines User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """represents a User

    Attributes:
        email (str): email of user
        password (str): password of user
        first_name (str): first name of user
        last_name (str): last name of user
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
