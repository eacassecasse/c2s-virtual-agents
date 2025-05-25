#!/usr/bin/python
""" holds class Brand"""
import app.models as models
from app.models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Brand(BaseModel, Base):
    """Representation of Brand """
    if models.storage_t == 'db':
        __tablename__ = 'brands'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Brand"""
        super().__init__(*args, **kwargs)
