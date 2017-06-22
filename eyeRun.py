
# coding: utf-8

# In[2]:


from sklearn.svm import SVC
import numpy as np
import pandas as pd
import pickle


# In[63]:


# read names that have provided survey eye color data
columns = ['name', 'left', 'right', 'left_desc', 'right_desc']
data = pd.read_csv("PGP-eyecolor.csv", names=columns)
dataNames = data['name'].values.tolist()


# In[72]:


# load numpy arrays from Arvados collection
names = np.load("names.npy")
pgp = np.load("hiq-pgp.npy")
for i in range(len(names)):
    names[i] = names[i][:8]


# In[101]:


nameIndices = []
for i in range(len(names)):
    if names[i] in dataNames:
        nameIndices.append(i)
        
knownData = pgp[nameIndexes]
unknownData = np.delete(pgp, nameIndices)
unknownData.reshape(len(names), knownData.shape[1] - 1)


# In[ ]:


print knownData.shape
print unknownData.shape


# In[ ]:




