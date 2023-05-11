#!/usr/bin/python3
"""defines BaseModel class"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """represents BaseModel"""

    def __init__(self, *args, **kwargs):
        """initialize new BaseModel object

        Args:
            *args (any): Unused
            **kwargs (dict): Keys/values pairs of attributes
        """
        dtformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, dtformat)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """update updated_at with the current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """returns the dictionary of BaseModel instance.

        includeing keys/values pairs, __class__ represents
        the class name of an object.
        """
        copy_dict = self.__dict__.copy()
        copy_dict["created_at"] = self.created_at.isoformat()
        copy_dict["updated_at"] = self.updated_at.isoformat()
        copy_dict["__class__"] = self.__class__.__name__
        return copy_dict

    def __str__(self):
        """returns str repre of BaseModel instance"""
        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)
