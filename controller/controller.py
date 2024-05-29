import os
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from controller.task_manager import TaskManager, background_task
from model.model import Model
from mongodb.storage import DatabaseApplication
import uuid
import csv


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
            difficulty_breathing = patient.difficulty_breathing
            fatigue = patient.fatigue
            cough = patient.cough
            fever = patient.fever
            disease = patient.disease if patient.disease is not None else "-"
            self.model.patient_list.append(patient_id=patient_id, patient_name=patient_name, sex=sex, age=age,
                                           cholesterol_level=cholesterol_level, blood_pressure=blood_pressure,
                                           difficulty_breathing=difficulty_breathing, fatigue=fatigue, cough=cough,
                                           fever=fever, disease=disease)
        ml_path = Path(__file__).resolve().parent.parent / "ml"
        self.rfr = joblib.load(os.path.join(ml_path, "rfr_model.pkl"))
        self.ml_model = load_model(os.path.join(ml_path, 'checkpoint.keras'))
        df = pd.read_csv(os.path.join(ml_path, "Disease_symptom_and_patient_profile_dataset.csv"))
        self.target = df["Disease"]
        df = df.iloc[:, 1:]
        x_train, x_test, y_train, y_test = train_test_split(df.iloc[:, :8], df.iloc[:, -1], test_size=0.15)
        self.oe = OrdinalEncoder(categories=[["No", 'Yes']])
        self.oe.fit_transform(x_train["Fever"].array.reshape(-1, 1))
        self.be = OrdinalEncoder(categories=[["No", 'Yes']])
        self.be.fit_transform(x_train["Cough"].array.reshape(-1, 1))
        self.ce = OrdinalEncoder(categories=[["No", 'Yes']])
        self.ce.fit_transform(x_train["Fatigue"].array.reshape(-1, 1))
        self.de = OrdinalEncoder(categories=[["No", 'Yes']])
        self.de.fit_transform(x_train["Difficulty Breathing"].array.reshape(-1, 1))
        self.fe = OrdinalEncoder(categories=[['Low', 'Normal', "High"]])
        self.fe.fit_transform(x_train["Blood Pressure"].array.reshape(-1, 1))
        self.ge = OrdinalEncoder(categories=[['Low', 'Normal', "High"]])
        self.ge.fit_transform(x_train["Cholesterol Level"].array.reshape(-1, 1))
        self.ohe = OneHotEncoder(drop='first', sparse_output=False)
        self.ohe.fit_transform(x_train['Gender'].array.reshape(-1, 1))
        self.le = LabelEncoder()
        self.le.fit(self.target)

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
        patient_id = str(uuid.uuid4())
        disease = self.predict({'fever': fever,
                                'cough': cough,
                                'fatigue': fatigue,
                                'difficulty_breathing': difficulty_breathing,
                                'blood_pressure': blood_pressure,
                                'age': age,
                                'cholesterol_level': cholesterol_level,
                                'sex': sex})
        if not self.model.patient_list.contains(patient_id):
            self.model.patient_list.append(patient_id=patient_id, patient_name=patient_name, sex=sex, age=age,
                                           cholesterol_level=cholesterol_level,
                                           blood_pressure=blood_pressure, difficulty_breathing=difficulty_breathing,
                                           fatigue=fatigue, cough=cough, fever=fever,
                                           disease=disease)
        self.db_app.patients.add_or_update_patient(patient_id, patient_name, age, sex, cholesterol_level,
                                                   blood_pressure, difficulty_breathing, fatigue, cough,
                                                   fever, disease)

    def predict(self, symptoms):
        symptoms['fever'] = float(symptoms["fever"])
        symptoms['cough'] = float(symptoms["cough"])
        symptoms['fatigue'] = float(symptoms["fatigue"])
        symptoms['difficulty_breathing'] = float(symptoms["difficulty_breathing"])
        symptoms['blood_pressure'] = self.fe.transform([[symptoms["blood_pressure"]]])[0][0]
        symptoms['age'] = int(symptoms['age'])
        symptoms['cholesterol_level'] = self.ge.transform([[symptoms["cholesterol_level"]]])[0][0]
        symptoms['sex'] = self.ohe.transform([[symptoms['sex']]])[0][0]
        symptoms = [list(symptoms.values())]

        prediction = self.rfr.predict(symptoms)

        if prediction[0] == 0:
            return 'Healthy'
        else:
            net_pred = self.ml_model.predict(np.array(symptoms))
            return self.le.classes_[np.argmax(net_pred, axis=-1)[0]]

    @Slot(list)
    @background_task
    def remove_patients(self, patients):
        for patient_id in patients:
            self.model.patient_list.remove(patient_id)
            self.db_app.patients.delete(patient_id)

    @Slot(str)
    @background_task
    def export_to_csv(self, path):
        with open(os.path.join(path, f"{datetime.now().isoformat()}.csv"), mode='w', newline='',
                  encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["patient_id", "patient_name", "sex", "age", "cholesterol_level",
                                                      "blood_pressure", "difficulty_breathing", "fatigue", "cough",
                                                      "fever", "disease"])
            writer.writeheader()
            for patient in self.model.patient_list._patients:
                writer.writerow(
                    {"patient_id": patient.patient_id, "patient_name": patient.patient_name, "sex": patient.sex,
                     "age": patient.age, "cholesterol_level": patient.cholesterol_level,
                     "blood_pressure": patient.blood_pressure, "difficulty_breathing": patient.difficulty_breathing,
                     "fatigue": patient.fatigue, "cough": patient.cough,
                     "fever": patient.fever, "disease": patient.disease})
