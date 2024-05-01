#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity, "City": City,
    "Place": Place, "Review": Review,
    "State": State, "User": User
}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

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
            self.save()

    def reload(self):
        """Creates all tables in the database and the current
        database session."""
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )

        self.__session = scoped_session(session_factory)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def count(self, cls=None) -> int:
        """
        Returns the number of objects in the storage.

        Args:
            cls (optional): The class name of the objects to count.
            If not provided, counts all objects.

        Returns:
            int: The number of objects in the storage.
        """
        return len(self.all(cls))

    def get(self, cls=None, cls_id=None):
        """
        Returns the instance object that has the specified class name and id.

        Args:
            cls (optional): The class name of the object to retrieve.
            cls_id(optional): The ID of the object

        Returns:
            int: The number of objects in the storage.
        """
        if cls and cls_id:
            return self.__session.query(cls).filter(cls.id == cls_id).first()
        return None

    def drop_all_tables(self):
        """Drops all tables, useful when testing."""
        self.__engine.execute('SET FOREIGN_KEY_CHECKS = 0')
        self.__session.rollback()
        Base.metadata.drop_all(self.__engine)
        self.__engine.execute('SET FOREIGN_KEY_CHECKS = 1')
        self.reload()
