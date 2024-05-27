from typing import Dict

from pymongo.collection import Collection

from mongodb.models.base_crud import BaseCRUD, db_connection_error_handler


class Patient(BaseCRUD):
    def __init__(self, collection: Collection, patient_id: str, connector):
        # set collection and connector manually because of patient_id
        self.collection = collection[patient_id]
        self.connector = connector

        self.id = patient_id

    @property
    def patient_name(self) -> str:
        return self._get()

    @patient_name.setter
    def patient_name(self, value: str):
        self._set(value)

    @property
    def sex(self) -> str:
        return self._get()

    @sex.setter
    def sex(self, value: str):
        self._set(value)

    @property
    def age(self) -> int:
        return self._get()

    @age.setter
    def age(self, value: int):
        self._set(value)

    @property
    def cholesterol_level(self) -> str:
        return self._get()

    @cholesterol_level.setter
    def cholesterol_level(self, value: str):
        self._set(value)

    @property
    def blood_pressure(self) -> str:
        return self._get()

    @blood_pressure.setter
    def blood_pressure(self, value: str):
        self._set(value)

    @property
    def difficulty_breathing(self) -> bool:
        return self._get()

    @difficulty_breathing.setter
    def difficulty_breathing(self, value: bool):
        self._set(value)

    @property
    def fatigue(self) -> bool:
        return self._get()

    @fatigue.setter
    def fatigue(self, value: bool):
        self._set(value)

    @property
    def cough(self) -> bool:
        return self._get()

    @cough.setter
    def cough(self, value: bool):
        self._set(value)

    @property
    def fever(self) -> bool:
        return self._get()

    @fever.setter
    def fever(self, value: bool):
        self._set(value)

    @property
    def disease(self) -> bool:
        return self._get()

    @disease.setter
    def disease(self, value: bool):
        self._set(value)

    def __str__(self):
        return f"Patient object {self.id}"

    def __repr__(self):
        return f"Patient object {self.id}"


class Patients(Dict[str, Patient]):
    def __init__(self, collection: Collection, connector):
        self.collection = collection['patients']
        self.connector = connector
        self.load_patients()

    def add_or_update_patient(self, patient_id: str, patient_name: str, age: int, sex: str, cholesterol_level: str,
                              blood_pressure: str, difficulty_breathing: bool, fatigue: bool, cough: bool,
                              fever: bool, disease: str) -> Patient:
        """Save patient into the database, and return Patient class"""
        if patient_id in self.keys():
            print(f"Patient with id '{patient_id}' already added. Updating existent patient.")
            patient = self[patient_id]
            patient.patient_name = patient_name
            patient.update({
                "patient_name": patient_name,
                "sex": sex, "age": age, "cholesterol_level": cholesterol_level, "blood_pressure": blood_pressure,
                "difficulty_breathing": difficulty_breathing, "fatigue": fatigue, "cough": cough, "fever": fever,
                "disease": disease
            })
        else:
            patient = Patient(self.collection, patient_id, self.connector)
            patient.new({
                "patient_name": patient_name,
                "sex": sex, "age": age, "cholesterol_level": cholesterol_level, "blood_pressure": blood_pressure,
                "difficulty_breathing": difficulty_breathing, "fatigue": fatigue, "cough": cough, "fever": fever,
                "disease": disease
            })
            self[patient_id] = patient
        return patient

    @db_connection_error_handler
    def load_patients(self):
        """Load all patients from the database"""
        self.clear()

        for pdata in self.collection.database.list_collection_names():
            try:
                # pdata has look like "patient.AVCD1234.foo" 1 index is correspond patient id
                patient_id = pdata.split(".")[1]
                if patient_id not in self.keys():
                    self[patient_id] = Patient(self.collection, patient_id, self.connector)
            except IndexError:
                pass
        print(f"Loaded patients: {len(self.keys())}")

    def delete(self, patient_id: str) -> int:
        """
        Delete patient from database
        :return: number of deleted collection
        """
        delete_field_count = 0
        try:
            del self[patient_id]
            db = self.collection.database
            for collection_name in db.list_collection_names():
                if patient_id in collection_name:
                    db.drop_collection(collection_name)
                    delete_field_count += 1
                    print(f"Collection '{collection_name}' has been deleted")
        except KeyError:
            pass
        return delete_field_count
