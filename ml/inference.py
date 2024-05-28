#!/usr/bin/env python
# coding: utf-8

# In[1]:


import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf


df = pd.read_csv("Disease_symptom_and_patient_profile_dataset.csv")
target=df["Disease"]
df = df.iloc[:,1:]

x_train,x_test,y_train,y_test = train_test_split(df.iloc[:,:8],df.iloc[:,-1], test_size=0.15)

oe = OrdinalEncoder(categories=[['No','Yes']])
x_train_fever = oe.fit_transform(x_train["Fever"].array.reshape(-1, 1))
be = OrdinalEncoder(categories=[['No','Yes']])
x_train_cough = be.fit_transform(x_train["Cough"].array.reshape(-1, 1))
ce = OrdinalEncoder(categories=[['No','Yes']])
x_train_fat = ce.fit_transform(x_train["Fatigue"].array.reshape(-1, 1))
de = OrdinalEncoder(categories=[['No','Yes']])
x_train_breath = de.fit_transform(x_train["Difficulty Breathing"].array.reshape(-1, 1))
fe = OrdinalEncoder(categories=[['Low','Normal',"High"]])
x_train_blood = fe.fit_transform(x_train["Blood Pressure"].array.reshape(-1, 1))
ge = OrdinalEncoder(categories=[['Low','Normal',"High"]])
x_train_chol = ge.fit_transform(x_train["Cholesterol Level"].array.reshape(-1, 1))
ohe = OneHotEncoder(drop='first',sparse_output=False)
x_train_gender = ohe.fit_transform(x_train['Gender'].array.reshape(-1, 1))


le = LabelEncoder()
le.fit(target)


# In[2]:


def make_inference(model_path:str, symptoms:dict):
    '''
    Значення в словнику мають обовязково йти в такому порядку:
    Fever, Cough, Fatigue, Difficulty Breathing, Blood Pressure, Age, Cholesterol Level, Gender
    '''
    
    symptoms['Fever']= oe.transform([[symptoms["Fever"]]])[0][0]
    symptoms['Cough']=be.transform([[symptoms["Cough"]]])[0][0]
    symptoms['Fatigue']=ce.transform([[symptoms["Fatigue"]]])[0][0]
    symptoms['Difficulty Breathing']=de.transform([[symptoms["Difficulty Breathing"]]])[0][0]
    symptoms['Blood Pressure']= fe.transform([[symptoms["Blood Pressure"]]])[0][0]
    symptoms['Age']=int(symptoms['Age'])
    symptoms['Cholesterol Level']=ge.transform([[symptoms["Cholesterol Level"]]])[0][0]
    symptoms['Gender']=ohe.transform([[symptoms['Gender']]])[0][0]
    
    symptoms=[list(symptoms.values())]
    
    numbers = [str(int(num)) for num in symptoms[0]]
    conumbers = ''.join(numbers)
    np.random.seed(int(conumbers))
    
    rfr=joblib.load(model_path)
    
    prediction=rfr.predict(symptoms)
    if prediction[0]==0:
        return 'The patient is healthy!!!'
    else: 
        model=load_model('checkpoint')
        net_pred= model.predict(symptoms)
        return le.classes_[np.argmax(net_pred, axis = -1)[0]]


# In[3]:


data={
    'Fever': 'Yes',
    'Cough':'No',
    'Fatigue':'Yes',
    'Difficulty Breathing':'Yes',
    'Age': 20,
    'Gender': 'Female',
    'Blood Pressure':'High',
    'Cholesterol Level' : 'High',
    
}
print(make_inference('rfr_model.pkl',data) )


# In[4]:


data={
    'Fever': 'Yes',
    'Cough':'Yes',
    'Fatigue':'Yes',
    'Difficulty Breathing':'Yes',
    'Age': 50,
    'Gender': 'Male',
    'Blood Pressure':'Low',
    'Cholesterol Level' : 'Low'
}
print(make_inference('rfr_model.pkl',data) )


# In[ ]:




