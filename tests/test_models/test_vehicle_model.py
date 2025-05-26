#!/usr/bin/python3
"""
Contains the TestVehicleModelDocs classes
"""

import inspect
import app.models
from app.models import vehicle_model
from app.models.base_model import BaseModel
import pep8
import unittest
VehicleModel = vehicle_model.VehicleModel


class TestVehicleModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of VehicleModel class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.vehicle_model_f = inspect.getmembers(VehicleModel,
                                                 inspect.isfunction)

    def test_pep8_conformance_vehicle_model(self):
        """Test that app/models/vehicle_model.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['app/models/vehicle_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_vehicle_model(self):
        """
        Test that tests/test_models/test_vehicle_model.py conforms
        to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_vehicle_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_vehicle_model_module_docstring(self):
        """Test for the vehicle_model.py module docstring"""
        self.assertIsNot(vehicle_model.__doc__, None,
                         "vehicle_model.py needs a docstring")
        self.assertTrue(len(vehicle_model.__doc__) >= 1,
                        "vehicle_model.py needs a docstring")

    def test_vehicle_model_class_docstring(self):
        """Test for the VehicleModel class docstring"""
        self.assertIsNot(VehicleModel.__doc__, None,
                         "VehicleModel class needs a docstring")
        self.assertTrue(len(VehicleModel.__doc__) >= 1,
                        "VehicleModel class needs a docstring")

    def test_vehicle_model_func_docstrings(self):
        """Test for the presence of docstrings in VehicleModel methods"""
        for func in self.vehicle_model_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestVehicleModel(unittest.TestCase):
    """Test the VehicleModel class"""
    def test_is_subclass(self):
        """Test that VehicleModel is a subclass of BaseModel"""
        vehicle_model = VehicleModel()
        self.assertIsInstance(vehicle_model, BaseModel)
        self.assertTrue(hasattr(vehicle_model, "id"))
        self.assertTrue(hasattr(vehicle_model, "created_at"))
        self.assertTrue(hasattr(vehicle_model, "updated_at"))

    def test_name_attr(self):
        """
        Test that VehicleModel has attribute name, and it's
        an empty string"""
        vehicle_model = VehicleModel()
        self.assertTrue(hasattr(vehicle_model, "name"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle_model.name, None)
        else:
            self.assertEqual(vehicle_model.name, "")

    def test_state_id_attr(self):
        """
        Test that VehicleModel has attribute state_id, and it's
        an empty string"""
        vehicle_model = VehicleModel()
        self.assertTrue(hasattr(vehicle_model, "brand_id"))
        if app.models.storage_t == 'db':
            self.assertEqual(vehicle_model.brand_id, None)
        else:
            self.assertEqual(vehicle_model.brand_id, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        c = VehicleModel()
        new_d = c.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_brand" in new_d)
        for attr in c.__dict__:
            if attr != "_sa_instance_brand":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        c = VehicleModel()
        new_d = c.to_dict()
        self.assertEqual(new_d["__class__"], "VehicleModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], c.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], c.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        vehicle_model = VehicleModel()
        string = "[VehicleModel] ({}) {}".format(vehicle_model.id,
                                                 vehicle_model.__dict__)
        self.assertEqual(string, str(vehicle_model))
