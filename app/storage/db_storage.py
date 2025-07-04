#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import app.models as models
from app.models.base_model import Base
from app.models.brand import Brand
from app.models.vehicle_model import VehicleModel
from app.models.vehicle import Vehicle
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

classes = {"Brand": Brand, "VehicleModel": VehicleModel, "Vehicle": Vehicle}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        C2S_MYSQL_USER = getenv('C2S_MYSQL_USER')
        C2S_MYSQL_PWD = getenv('C2S_MYSQL_PWD')
        C2S_MYSQL_HOST = getenv('C2S_MYSQL_HOST')
        C2S_MYSQL_DB = getenv('C2S_MYSQL_DB')
        C2S_ENV = getenv('C2S_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(C2S_MYSQL_USER,
                                             C2S_MYSQL_PWD,
                                             C2S_MYSQL_HOST,
                                             C2S_MYSQL_DB))
        if C2S_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def start_transaction(self):
        """ Begins a new transaction """
        self.__session.begin()

    def commit(self):
        """ Commits the current transaction """
        self.__session.commit()

    def rollback(self):
        """ Rollback the current transaction """
        self.__session.rollback()

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def delete_all(self, cls):
        """ Deletes all records from a provided class """
        self.__session.query(cls).delete()

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
