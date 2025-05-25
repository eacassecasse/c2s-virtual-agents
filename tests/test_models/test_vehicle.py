#!/usr/bin/python3
"""
Contains the TestVehicleDocs classes
"""

from datetime import datetime
import inspect
import app.models
from app.models import vehicle
from app.models.base_model import BaseModel
from app.models.vehicle import DriveTrainType
from app.models.vehicle import FuelType
from app.models.vehicle import TransmissionType
import pep8
import unittest
Vehicle = vehicle.Vehicle


class TestVehicleDocs(unittest.TestCase):
    """Tests to check the documentation and style of Vehicle class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.vehicle_f = inspect.getmembers(Vehicle, inspect.isfunction)

    def test_pep8_conformance_vehicle(self):
        """Test that app/models/vehicle.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['app/models/vehicle.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_vehicle(self):
        """Test that tests/test_models/test_vehicle.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_vehicle.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_vehicle_module_docstring(self):
        """Test for the vehicle.py module docstring"""
        self.assertIsNot(vehicle.__doc__, None,
                         "vehicle.py needs a docstring")
        self.assertTrue(len(vehicle.__doc__) >= 1,
                        "vehicle.py needs a docstring")

    def test_vehicle_class_docstring(self):
        """Test for the Vehicle class docstring"""
        self.assertIsNot(Vehicle.__doc__, None,
                         "Vehicle class needs a docstring")
        self.assertTrue(len(Vehicle.__doc__) >= 1,
                        "Vehicle class needs a docstring")

    def test_vehicle_func_docstrings(self):
        """Test for the presence of docstrings in Vehicle methods"""
        for func in self.vehicle_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestVehicle(unittest.TestCase):
    """Test the Vehicle class"""
    def test_is_subclass(self):
        """Test that Vehicle is a subclass of BaseModel"""
        vehicle = Vehicle()
        self.assertIsInstance(vehicle, BaseModel)
        self.assertTrue(hasattr(vehicle, "id"))
        self.assertTrue(hasattr(vehicle, "created_at"))
        self.assertTrue(hasattr(vehicle, "updated_at"))

    def test_vehicle_model_id_attr(self):
        """Test Vehicle has attr vehicle_model_id, and it's an empty string"""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "model_id"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.model_id, None)
        else:
            self.assertEqual(vehicle.model_id, "")

    def test_license_plate_attr(self):
        """Test Vehicle has attr license_plate, and it's an empty string"""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "license_plate"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.license_plate, None)
        else:
            self.assertEqual(vehicle.license_plate, "")

    def test_engine_number_attr(self):
        """Test Vehicle has attr engine_number, and it's an empty string"""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "engine_number"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.engine_number, None)
        else:
            self.assertEqual(vehicle.engine_number, "")

    def test_chassis_number_attr(self):
        """Test Vehicle has attr chassis_number, and it's an empty string"""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "chassis_number"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.chassis_number, None)
        else:
            self.assertEqual(vehicle.chassis_number, "")

    def test_year_of_manufacture_attr(self):
        """Test Vehicle has attr year_of_manufacture, and it's an int == 0"""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "year_of_manufacture"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.year_of_manufacture, None)
        else:
            self.assertEqual(type(vehicle.year_of_manufacture), int)
            self.assertEqual(vehicle.year_of_manufacture, 0)

    def test_mileage_attr(self):
        """Test Vehicle has attr mileage, and it's a float == 0.0"""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "mileage"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.mileage, None)
        else:
            self.assertEqual(type(vehicle.mileage), float)
            self.assertEqual(vehicle.mileage, 0.0)

    def test_color_attr(self):
        """Test Vehicle has attr color, and it's an empty string"""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "color"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.color, None)
        else:
            self.assertEqual(vehicle.color, "")

    def test_registration_date_attr(self):
        """Test Vehicle has attr registration_date, and it's an empty string"""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "registration_date"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.registration_date, None)
        else:
            self.assertEqual(vehicle.registration_date, "")

    def test_fuel_type_attr(self):
        """
        Test Vehicle has attr fuel_type, and it's equals
        a FuelType = Petrol
        """
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "fuel_type"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.fuel_type, None)
        else:
            self.assertEqual(type(vehicle.fuel_type), FuelType)
            self.assertEqual(vehicle.fuel_type, FuelType.PETROL)

    def test_transmission_type_attr(self):
        """
        Test Vehicle has attr transmission_type, and it's equals
        to a TransmissionType = Automatic
        """
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "transmission_type"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.transmission_type, None)
        else:
            self.assertEqual(type(vehicle.transmission_type), TransmissionType)
            self.assertEqual(vehicle.transmission_type,
                             TransmissionType.AUTOMATIC)

    def test_drivetrain_type_attr(self):
        """
        Test Vehicle has attr drivetrain_type, and it's equals
        to a DriveTrainType = FWD
        """
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, "drivetrain_type"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle.drivetrain_type, None)
        else:
            self.assertEqual(type(vehicle.drivetrain_type), DriveTrainType)
            self.assertEqual(vehicle.drivetrain_type, DriveTrainType.FWD)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        p = Vehicle()
        new_d = p.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in p.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        p = Vehicle()
        new_d = p.to_dict()
        self.assertEqual(new_d["__class__"], "Vehicle")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], p.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], p.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        vehicle = Vehicle()
        string = "[Vehicle] ({}) {}".format(vehicle.id, vehicle.__dict__)
        self.assertEqual(string, str(vehicle))
