from PyQt6.QtCore import QObject, pyqtProperty as Property, QThreadPool, QMutex, QRunnable, QMutexLocker, QThread, \
    QTimer
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

from controller.task_manager import TaskManager, background_task
from model.model import Model


class Controller(TaskManager):
    messageSignal = Signal(str, str, str, arguments=['message', 'description', 'window_type'])

    def __init__(self, model: Model):
        super().__init__()
        self.model = model

    @Slot(str, int, str, str, str, bool, bool, bool, bool, result=QObject)
    @background_task
    def add_patient(self, patient_name: str, age: int, sex: str, cholesterol_level: str, blood_pressure: str,
                    difficulty_breathing: bool, fatigue: bool, cough: bool, fever: bool):
        print(patient_name, age, sex, cholesterol_level, blood_pressure, difficulty_breathing, fatigue, cough, fever)
        self.model.patient_list.append(patient_name=patient_name, sex=sex, age=age, cholesterol_level=cholesterol_level,
                                       blood_pressure=blood_pressure, difficulty_breathing=difficulty_breathing,
                                       fatigue=fatigue, cough=cough, fever=fever,
                                       disease="some")
