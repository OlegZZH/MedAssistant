#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install pandas
# !pip install scikit-learn
# !conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0 -y
# !python -m pip install "tensorflow<2.11"


# In[2]:


import pandas as pd
import numpy as np
import joblib
import keras
import tensorflow as tf


# In[3]:


print(tf.config.list_physical_devices('GPU'))


# In[4]:


np.random.seed(9)


# In[5]:


df = pd.read_csv("Disease_symptom_and_patient_profile_dataset.csv")


# In[6]:


df.info()


# In[7]:


df.head()


# In[8]:


df.nunique()


# In[9]:


disease_list=df['Disease']


# In[10]:


df = df.drop('Outcome Variable', axis=1)
df.head()


# In[11]:


target=df.pop("Disease")
df.head()


# In[12]:


df["Fever"]=df["Fever"].map({"No":0,"Yes":1})
df["Cough"]=df["Cough"].map({"No":0,"Yes":1})
df["Fatigue"]=df["Fatigue"].map({"No":0,"Yes":1})
df["Difficulty Breathing"]=df["Difficulty Breathing"].map({"No":0,"Yes":1})
df["Gender"]=df["Gender"].map({"Female":0,"Male":1})
df["Blood Pressure"]=df["Blood Pressure"].map({"Low":0,"Normal":1, "High":2})
df["Cholesterol Level"]=df["Cholesterol Level"].map({"Low":0,"Normal":1, "High":2})
# df["Outcome Variable"]=df["Outcome Variable"].map({"Negative":0,"Positive":1})
df.head()


# In[13]:


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
le.fit(target)
target=le.transform(target)


# In[14]:


dataset=tf.data.Dataset.from_tensor_slices((df.values,target))


# In[15]:


for feature,label in dataset.take(5):
  print(feature,label)


# In[16]:


train_dataset=dataset.take(330)
test_dataset=dataset.skip(330)


# In[17]:


train_dataset=train_dataset.shuffle(len(train_dataset)).batch(10)
test_dataset=test_dataset.shuffle(len(test_dataset)).batch(10)


# In[18]:


checkpoint_filepath='checkpoint'
model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    monitor='val_accuracy',
    mode='max',
    verbose=1,
    save_best_only=True)


# In[ ]:


model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(116)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_dataset, validation_data=test_dataset, epochs=30, callbacks=[model_checkpoint_callback])


# In[ ]:




