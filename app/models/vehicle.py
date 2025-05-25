#!/usr/bin/python
""" holds class Vehicle"""
import enum
import app.models as models
from app.models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import (Column, String, Float, Integer,
                        DateTime, ForeignKey, Enum)


class FuelType(enum.Enum):
    """Fuel types"""
    PETROL = "Petrol"
    DIESEL = "Diesel"
    ELECTRIC = "Electric"
    HYBRID = "Hybrid"


class TransmissionType(enum.Enum):
    """Transmission types"""
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"
    CVT = "CVT"
    IMT = "iMT"


class DriveTrainType(enum.Enum):
    """Drive train types"""
    FWD = "FWD"
    RWD = "RWD"
    AWD = "AWD"
    _4WD = "4WD"


class Vehicle(BaseModel, Base):
    """Representation of Vehicle """
    if models.storage_t == 'db':
        __tablename__ = 'vehicles'
        model_id = Column(
            String(60),
            ForeignKey('vehicle_models.id'),
            nullable=False)
        license_plate = Column(String(11), nullable=False)
        engine_number = Column(String(21), nullable=False)
        chassis_number = Column(String(21), nullable=False)
        color = Column(String(21), nullable=False)
        year_of_manufacture = Column(Integer(), nullable=False)
        mileage = Column(Float(2), nullable=False)
        registration_date = Column(DateTime, nullable=True)
        fuel_type = Column(
            Enum(FuelType),
            nullable=False,
            default=FuelType.PETROL)
        transmission_type = Column(
            Enum(TransmissionType),
            nullable=False,
            default=TransmissionType.AUTOMATIC)
        drivetrain_type = Column(
            Enum(DriveTrainType),
            nullable=False,
            default=DriveTrainType.FWD)
    else:
        model_id = ""
        license_plate = ""
        engine_number = ""
        chassis_number = ""
        color = ""
        year_of_manufacture = 0
        mileage = 0.0
        registration_date = ""
        fuel_type = FuelType.PETROL
        transmission_type = TransmissionType.AUTOMATIC
        drivetrain_type = DriveTrainType.FWD

    def __init__(self, *args, **kwargs):
        """initializes Vehicle"""
        super().__init__(*args, **kwargs)
