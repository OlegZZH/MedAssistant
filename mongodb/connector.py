import pymongo
from PyQt6.QtCore import QObject, pyqtProperty as Property
from PyQt6.QtCore import pyqtSignal as Signal
from pymongo.errors import ServerSelectionTimeoutError


class Connector(QObject):
    connection_changed = Signal(bool)

    def __init__(self, db_timeout_ms: int = 1000):
        super().__init__()
        default_connection_options = {
            'connectTimeoutMS': db_timeout_ms,
            'serverSelectionTimeoutMS': db_timeout_ms
        }
        self.client = pymongo.MongoClient(**default_connection_options)
        self._connected = True

    def activate(self):
        """
        It's not really the method to connect.
        The connection must be activated before in the __init__ method.
        This method check if connection is ok,
        and emmit signal if there is a problem with connection.
        """
        try:
            self.client.server_info()
            self.connected = True
        except ServerSelectionTimeoutError:
            self.connected = False

    @Property(bool, notify=connection_changed)
    def connected(self) -> bool:
        return self._connected

    @connected.setter
    def connected(self, new_value: bool):
        if self._connected != new_value and new_value is not None:
            self._connected = new_value
            self.connection_changed.emit(new_value)
