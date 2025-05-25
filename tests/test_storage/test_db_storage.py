#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
import app.models
from app.models import storage
from app.storage import db_storage
from app.models.base_model import BaseModel
from app.models.brand import Brand
from app.models.vehicle_model import VehicleModel
from app.models.vehicle import Vehicle
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Brand": Brand, "VehicleModel": VehicleModel, "Vehicle": Vehicle}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that app/storage/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['app/storage/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_storage/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_storage/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(app.models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(app.models.storage.all()), dict)

    @unittest.skipIf(app.models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(app.models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(app.models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(app.models.storage_t != 'db', "not testing db storage")
    def test_get_db(self):
        """ Tests method for obtaining an instance db storage"""
        dic = {"name": "Toyota"}
        instance = Brand(**dic)
        storage.new(instance)
        storage.save()
        get_instance = storage.get(Brand, instance.id)
        self.assertEqual(get_instance, instance)

    @unittest.skipIf(app.models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """ Tests count method db storage """
        dic = {"name": "Nissan"}
        brand = Brand(**dic)
        storage.new(brand)
        dic = {"name": "Mexico", "brand_id": brand.id}
        vehicle_model = VehicleModel(**dic)
        storage.new(vehicle_model)
        storage.save()
        c = storage.count()
        self.assertEqual(len(storage.all()), c)
