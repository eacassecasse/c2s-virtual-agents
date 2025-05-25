#!/usr/bin/python
""" holds class VehicleModel"""
import app.models as models
from app.models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class VehicleModel(BaseModel, Base):
    """Representation of VehicleModel """
    if models.storage_t == 'db':
        __tablename__ = 'vehicle_models'
        brand_id = Column(String(60), ForeignKey('brands.id'), nullable=False)
        name = Column(String(128), nullable=False)
    else:
        brand_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes VehicleModel"""
        super().__init__(*args, **kwargs)
