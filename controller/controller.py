from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

from controller.task_manager import TaskManager, background_task
from model.model import Model
from mongodb.storage import DatabaseApplication
import uuid


class Controller(TaskManager):
    messageSignal = Signal(str, str, str, arguments=['message', 'description', 'window_type'])

    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self.db_app = DatabaseApplication("med_assistant")
        self.db_app.connector.connection_changed.connect(self.on_db_connection_changed)
        for patient_id, patient in self.db_app.patients.items():
            patient_name = patient.patient_name if patient.patient_name is not None else '-'
            sex = patient.sex if patient.sex is not None else '-'
            age = patient.age if patient.age is not None else 0
            cholesterol_level = patient.cholesterol_level if patient.cholesterol_level is not None else '-'
            blood_pressure = patient.blood_pressure if patient.blood_pressure is not None else '-'
            difficulty_breathing = patient.difficulty_breathing if patient.difficulty_breathing is not None else False
            fatigue = patient.fatigue if patient.fatigue is not None else False
            cough = patient.cough if patient.cough is not None else False
            fever = patient.fever if patient.fever is not None else False
            disease = patient.disease if patient.disease is not None else "-"
            self.model.patient_list.append(patient_id=patient_id, patient_name=patient_name, sex=sex, age=age,
                                           cholesterol_level=cholesterol_level, blood_pressure=blood_pressure,
                                           difficulty_breathing=difficulty_breathing, fatigue=fatigue, cough=cough,
                                           fever=fever, disease=disease)

    @Slot(bool)
    def on_db_connection_changed(self, connected: bool):
        if connected:
            print("Database is connected")
        else:
            msg = "Database connection is broken"
            print(msg)

    @Slot(str, int, str, str, str, bool, bool, bool, bool, result=QObject)
    @background_task
    def add_patient(self, patient_name: str, age: int, sex: str, cholesterol_level: str, blood_pressure: str,
                    difficulty_breathing: bool, fatigue: bool, cough: bool, fever: bool):
        print(patient_name, age, sex, cholesterol_level, blood_pressure, difficulty_breathing, fatigue, cough, fever)
        patient_id = str(uuid.uuid4())
        disease = "some"
        if not self.model.patient_list.contains(patient_id):
            self.model.patient_list.append(patient_id=patient_id, patient_name=patient_name, sex=sex, age=age,
                                           cholesterol_level=cholesterol_level,
                                           blood_pressure=blood_pressure, difficulty_breathing=difficulty_breathing,
                                           fatigue=fatigue, cough=cough, fever=fever,
                                           disease=disease)
        patient = self.db_app.patients.add_or_update_patient(patient_id, patient_name, age, sex, cholesterol_level,
                                                             blood_pressure, difficulty_breathing, fatigue, cough,
                                                             fever, disease)
        print(patient)
