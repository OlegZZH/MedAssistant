#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import joblib


# In[2]:


np.random.seed(9)


# In[3]:


df = pd.read_csv("Disease_symptom_and_patient_profile_dataset.csv")


# In[4]:


df.info()


# In[5]:


df.head()


# In[6]:


df.nunique()


# In[7]:


disease_list=df['Disease']


# In[8]:


df = df.iloc[:,1:]
df.head()


# In[9]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(df.iloc[:,:8],df.iloc[:,-1], test_size=0.15)


# In[10]:


from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder


# In[11]:


oe = OrdinalEncoder(categories=[['No','Yes']])
x_train_fever = oe.fit_transform(x_train["Fever"].array.reshape(-1, 1))
x_test_fever = oe.transform(x_test["Fever"].array.reshape(-1, 1))

be = OrdinalEncoder(categories=[['No','Yes']])
x_train_cough = be.fit_transform(x_train["Cough"].array.reshape(-1, 1))
x_test_cough = be.transform(x_test["Cough"].array.reshape(-1, 1))

ce = OrdinalEncoder(categories=[['No','Yes']])
x_train_fat = ce.fit_transform(x_train["Fatigue"].array.reshape(-1, 1))
x_test_fat = ce.transform(x_test["Fatigue"].array.reshape(-1, 1))

de = OrdinalEncoder(categories=[['No','Yes']])
x_train_breath = de.fit_transform(x_train["Difficulty Breathing"].array.reshape(-1, 1))
x_test_breath = de.transform(x_test["Difficulty Breathing"].array.reshape(-1, 1))

fe = OrdinalEncoder(categories=[['Low','Normal',"High"]])
x_train_blood = fe.fit_transform(x_train["Blood Pressure"].array.reshape(-1, 1))
x_test_blood = fe.transform(x_test["Blood Pressure"].array.reshape(-1, 1))

ge = OrdinalEncoder(categories=[['Low','Normal',"High"]])
x_train_chol = ge.fit_transform(x_train["Cholesterol Level"].array.reshape(-1, 1))
x_test_chol = ge.transform(x_test["Cholesterol Level"].array.reshape(-1, 1))

ohe = OneHotEncoder(drop='first',sparse_output=False)
x_train_gender = ohe.fit_transform(x_train['Gender'].array.reshape(-1, 1))
x_test_gender = ohe.transform(x_test['Gender'].array.reshape(-1, 1))

x_train_age = [[i]for i in x_train["Age"]]
x_train_age=np.array(x_train_age)
x_test_age = [[i]for i in x_test["Age"]] 
x_test_age=np.array(x_test_age)


# In[12]:


x_train_transformed = np.concatenate((x_train_fever,x_train_cough,x_train_fat,x_train_breath,x_train_age,x_train_gender,x_train_blood,x_train_chol),axis=1)

x_test_transformed = np.concatenate((x_test_fever,x_test_cough,x_test_fat,x_test_breath,x_test_age,x_test_gender,x_test_blood,x_test_chol),axis=1)


# In[13]:


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
le.fit(y_train)

y_train = le.transform(y_train)
y_test = le.transform(y_test)



# In[14]:


# from sklearn.neighbors import KNeighborsClassifier
# 

# knn = KNeighborsClassifier()
# knn.fit(x_train_transformed,y_train)

# kpred = knn.predict(x_test_transformed)
# accuracy_score(kpred,y_test)


# In[15]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

rfr = RandomForestClassifier()
rfr.fit(x_train_transformed,y_train)

fpred=rfr.predict(x_test_transformed)
accuracy_score(fpred,y_test)


# In[16]:


# x_test_transformed


# In[17]:


# joblib.dump(knn, "knn_model.pkl") 
joblib.dump(rfr, "rfr_model.pkl") 


# In[18]:


# rfr.predict([[ 0.,  0.,  1.,  0.,  1., 45.,  2.,  0.]])


# In[ ]:




