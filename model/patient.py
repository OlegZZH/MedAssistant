from dataclasses import dataclass
from typing import Optional, Any

from PyQt6.QtCore import QObject, pyqtProperty as Property, Qt, QAbstractListModel, QModelIndex
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

ROLE_PATIENT_ID = Qt.ItemDataRole.UserRole + 0
ROLE_NAME = Qt.ItemDataRole.UserRole + 1
ROLE_AGE = Qt.ItemDataRole.UserRole + 2
ROLE_SEX = Qt.ItemDataRole.UserRole + 3
ROLE_CHOLESTEROL_LEVEL = Qt.ItemDataRole.UserRole + 4
ROLE_BLOOD_PRESSURE = Qt.ItemDataRole.UserRole + 5
ROLE_DIFFICULTY_BREATHING = Qt.ItemDataRole.UserRole + 6
ROLE_FATIGUE = Qt.ItemDataRole.UserRole + 7
ROLE_COUGH = Qt.ItemDataRole.UserRole + 8
ROLE_FEVER = Qt.ItemDataRole.UserRole + 9
ROLE_DISEASE = Qt.ItemDataRole.UserRole + 10

patient_role_names = {
    ROLE_PATIENT_ID: b"patient_id",
    ROLE_NAME: b"patient_name",
    ROLE_AGE: b"age",
    ROLE_SEX: b"sex",
    ROLE_CHOLESTEROL_LEVEL: b"cholesterol_level",
    ROLE_BLOOD_PRESSURE: b"blood_pressure",
    ROLE_DIFFICULTY_BREATHING: b"difficulty_breathing",
    ROLE_FATIGUE: b"fatigue",
    ROLE_COUGH: b"cough",
    ROLE_FEVER: b"fever",
    ROLE_DISEASE: b"disease"
}


@dataclass
class PatientItem:
    patient_id: str = ""
    patient_name: str = ""
    age: int = 0
    sex: str = ""
    cholesterol_level: str = ""
    blood_pressure: str = ""
    difficulty_breathing: bool = False
    fatigue: bool = False
    cough: bool = False
    fever: bool = False
    disease: str = ""


class PatientList(QAbstractListModel):
    # NOTE:
    # The additional internal Signal-Slot connections are used ot make the list model thread safe.
    # See https://bugreports.qt.io/browse/QTBUG-60415 for more details.
    _append_signal = Signal(str, str, int, str, str, str, bool, bool, bool, bool, str)
    _remove_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._patients = []
        self._append_signal.connect(self._append_slot)
        self._remove_signal.connect(self._remove_slot)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Optional[str]:
        if not (0 <= index.row() < self.rowCount()):
            return

        if role == Qt.ItemDataRole.DisplayRole or role == ROLE_PATIENT_ID:
            return self._patients[index.row()].patient_id
        elif role == ROLE_NAME:
            return self._patients[index.row()].patient_name
        elif role == ROLE_AGE:
            return self._patients[index.row()].age
        elif role == ROLE_SEX:
            return self._patients[index.row()].sex
        elif role == ROLE_CHOLESTEROL_LEVEL:
            return self._patients[index.row()].cholesterol_level
        elif role == ROLE_BLOOD_PRESSURE:
            return self._patients[index.row()].blood_pressure
        elif role == ROLE_DIFFICULTY_BREATHING:
            return self._patients[index.row()].difficulty_breathing
        elif role == ROLE_FATIGUE:
            return self._patients[index.row()].fatigue
        elif role == ROLE_COUGH:
            return self._patients[index.row()].cough
        elif role == ROLE_FEVER:
            return self._patients[index.row()].fever
        elif role == ROLE_DISEASE:
            return self._patients[index.row()].disease

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if not (0 <= index.row() < self.rowCount()):
            return False

        if role == Qt.ItemDataRole.EditRole or role == ROLE_NAME:
            if type(value) is str:
                if self._patients[index.row()].patient_name != value:
                    self._patients[index.row()].patient_name = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_AGE:
            if type(value) is str:
                if self._patients[index.row()].age != value:
                    self._patients[index.row()].age = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_SEX:
            if type(value) is str:
                if self._patients[index.row()].sex != value:
                    self._patients[index.row()].sex = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_CHOLESTEROL_LEVEL:
            if type(value) is str:
                if self._patients[index.row()].cholesterol_level != value:
                    self._patients[index.row()].cholesterol_level = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_BLOOD_PRESSURE:
            if type(value) is bool:
                if self._patients[index.row()].blood_pressure != value:
                    self._patients[index.row()].blood_pressure = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_DIFFICULTY_BREATHING:
            if type(value) is bool:
                if self._patients[index.row()].difficulty_breathing != value:
                    self._patients[index.row()].difficulty_breathing = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_FATIGUE:
            if type(value) is bool:
                if self._patients[index.row()].fatigue != value:
                    self._patients[index.row()].fatigue = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_COUGH:
            if type(value) is bool:
                if self._patients[index.row()].cough != value:
                    self._patients[index.row()].cough = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_FEVER:
            if type(value) is bool:
                if self._patients[index.row()].fever != value:
                    self._patients[index.row()].fever = value
                    self.dataChanged.emit(index, index)
                return True
        elif role == ROLE_DISEASE:
            if type(value) is bool:
                if self._patients[index.row()].disease != value:
                    self._patients[index.row()].disease = value
                    self.dataChanged.emit(index, index)
                return True

        return False

    def roleNames(self) -> dict[int, bytes]:
        return patient_role_names

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._patients)

    @Slot(str, str, int, str, str, str, bool, bool, bool, bool, str)
    def _append_slot(self, patient_id, patient_name: str, age: int, sex: str, cholesterol_level: str,
                     blood_pressure: str,
                     difficulty_breathing: bool, fatigue: bool, cough: bool, fever: bool, disease: str):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._patients.insert(0, PatientItem(patient_id, patient_name, age, sex, cholesterol_level,
                                             blood_pressure, difficulty_breathing, fatigue, cough, fever, disease))
        self.endInsertRows()

    def append(self, patient_id: str, patient_name: str, age: int, sex: str, cholesterol_level: str,
               blood_pressure: str,
               difficulty_breathing: bool, fatigue: bool, cough: bool, fever: bool, disease: str):
        self._append_signal.emit(patient_id, patient_name, age, sex, cholesterol_level,
                                 blood_pressure, difficulty_breathing, fatigue, cough, fever, disease)

    @Slot(str)
    def _remove_slot(self, patient_id):
        for i, p in enumerate(self._patients):
            if p.patient_id == patient_id:
                self.beginRemoveRows(QModelIndex(), i, i)
                self._patients.remove(p)
                self.endRemoveRows()
                break

    def remove(self, patient_id):
        self._remove_signal.emit(patient_id)

    def remove_all(self):
        for patient_id in self._patients:
            self.remove(patient_id)
        self._patients = []

    def contains(self, patient_id) -> bool:
        for p in self._patients:
            if p.patient_id == patient_id:
                return True
        return False
