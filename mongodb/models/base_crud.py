import inspect
from dataclasses import dataclass

from pymongo.collection import Collection
from pymongo.errors import ServerSelectionTimeoutError

from mongodb.connector import Connector


def db_connection_error_handler(func):
    """
    Decorator to handle connection errors gracefully.

    If the decorated method raises any exception, it catches it, updates the connection status,
    and logs an appropriate message.

    Parameters:
    - func: The original method to be decorated.

    Returns:
    - The decorated method.
    """

    def wrapper(self, *args, **kwargs):
        if self.connector.connected:
            try:
                result = func(self, *args, **kwargs)
                return result
            except ServerSelectionTimeoutError:
                self.connector.connected = False

    return wrapper


@dataclass
class BaseCRUD:
    collection: Collection
    connector: Connector

    def __post_init__(self):
        """Update collection name, based on the class name"""
        self.collection = self.collection[self.collection_name]

    @property
    def collection_name(self):
        """this method converts the class name to lowercase"""
        return type(self).__name__.lower()

    @property
    def _field_name(self):
        """
        Extract the outer method's name. Name of the outer method must be the same as the collection's name
        """
        return inspect.currentframe().f_back.f_back.f_back.f_code.co_name

    @db_connection_error_handler
    def _get(self):
        """Get a value from collection, or None"""
        if result := self.collection.find_one():
            return result.get(self._field_name)

    @db_connection_error_handler
    def get_all_fields(self) -> dict:
        """Return all collection's fields"""
        # NOTE:
        #   Unused so far
        #   You should use this method when you want to get more than one field from a collection
        if data := self.collection.find_one():
            return data
        return {}

    @db_connection_error_handler
    def _set(self, value):
        """
        Update value in collection or insert if it does not exist.
        Also, it's possible to specify the name of the field to update
        """
        resp = self.collection.update_one({}, {"$set": {self._field_name: value}})
        if resp.matched_count == 0:
            self.collection.insert_one({self._field_name: value})

    @db_connection_error_handler
    def update(self, data: dict):
        """
        Update data in collection
        Use this method when you want to update more than one field
        """
        self.collection.update_one({}, {"$set": data}, upsert=True)

    @db_connection_error_handler
    def new(self, data: dict):
        """Insert new data into collection"""
        self.collection.insert_one(data)

    @db_connection_error_handler
    def drop(self):
        """Delete this collection"""
        self.collection.drop()
