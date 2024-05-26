from PyQt6.QtCore import QObject, pyqtProperty as Property
from PyQt6.QtCore import pyqtSignal as Signal

from .patient import PatientList


class Model(QObject):
    init_complete_changed = Signal(bool)
    initial_set_up_done_changed = Signal(bool)
    sw_version_changed = Signal(str)
    fw_version_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._patient_list = PatientList(self)

    def patient_list(self):
        return self._patient_list

    patient_list: PatientList = Property(QObject, patient_list, constant=True)
