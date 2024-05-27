from mongodb.connector import Connector
from mongodb.models.patient import Patients


class _Database:
    def __init__(self, db_name: str):
        self.connector = Connector()
        self.connector.activate()
        self.db = self.connector.client[db_name]
        self._db_name = db_name

    def delete_recursively(self, object_with_collection):
        """
        :parameter object_with_collection - Object that has a collection

        Deletes all collections with given name

        Example:
        delete_recursively(foo_collection)
        foo.one
        foo.two
        foo.any

        All collection that start from foo will be deleted
        """
        name = ".".join(object_with_collection.collection.full_name.split(".")[1::])
        for coll in self.db.list_collections():
            if coll["name"].startswith(name):
                self.db.drop_collection(coll["name"])

    def drop_db(self):
        """Drop current database collection"""
        self.connector.client.drop_database(self._db_name)


class DatabaseApplication(_Database):
    def __init__(self, db_name: str):
        super().__init__(db_name)

        self.patients = Patients(self.db, self.connector)
