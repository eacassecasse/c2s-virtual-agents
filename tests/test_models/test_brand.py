#!/usr/bin/python3
"""
Contains the TestBrandDocs classes
"""

import inspect
import app.models
from app.models import brand
from app.models.base_model import BaseModel
import pep8
import unittest

Brand = brand.Brand


class TestBrandDocs(unittest.TestCase):
    """Tests to check the documentation and style of Brand class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.brand_f = inspect.getmembers(Brand, inspect.isfunction)

    def test_pep8_conformance_brand(self):
        """Test that app/models/brand.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['app/models/brand.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_brand(self):
        """Test that tests/test_models/test_brand.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_brand.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_brand_module_docstring(self):
        """Test for the brand.py module docstring"""
        self.assertIsNot(brand.__doc__, None,
                         "brand.py needs a docstring")
        self.assertTrue(len(brand.__doc__) >= 1,
                        "brand.py needs a docstring")

    def test_brand_class_docstring(self):
        """Test for the Brand class docstring"""
        self.assertIsNot(Brand.__doc__, None,
                         "Brand class needs a docstring")
        self.assertTrue(len(Brand.__doc__) >= 1,
                        "Brand class needs a docstring")

    def test_brand_func_docstrings(self):
        """Test for the presence of docstrings in Brand methods"""
        for func in self.brand_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestBrand(unittest.TestCase):
    """Test the Brand class"""
    def test_is_subclass(self):
        """Test that Brand is a subclass of BaseModel"""
        brand = Brand()
        self.assertIsInstance(brand, BaseModel)
        self.assertTrue(hasattr(brand, "id"))
        self.assertTrue(hasattr(brand, "created_at"))
        self.assertTrue(hasattr(brand, "updated_at"))

    def test_name_attr(self):
        """Test that Brand has attribute name, and it's as an empty string"""
        brand = Brand()
        self.assertTrue(hasattr(brand, "name"))
        if app.models.storage_t == 'db':
            self.assertEqual(brand.name, None)
        else:
            self.assertEqual(brand.name, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        s = Brand()
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_brand" in new_d)
        for attr in s.__dict__:
            if attr != "_sa_instance_brand":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        s = Brand()
        new_d = s.to_dict()
        self.assertEqual(new_d["__class__"], "Brand")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], s.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], s.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        brand = Brand()
        string = "[Brand] ({}) {}".format(brand.id, brand.__dict__)
        self.assertEqual(string, str(brand))
