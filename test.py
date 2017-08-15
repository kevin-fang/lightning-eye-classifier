import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn import preprocessing
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import collections

# read names that have provided survey eye color data
columns = ['name', 'timestamp', 'id', 'blood_type', 'height', 'weight', 'hw_comments', 'left', 'right', 'left_desc', 'right_desc', 'eye_comments', 'hair', 'hair_desc', 'hair_comments', 'misc', 'handedness']

# pgp eye color data from survey
surveyData = pd.read_csv("./eye_color_data/PGP-Survey.csv", names=columns, na_values=['nan', '', 'NaN'])

# names of the pgp participants
surveyNames = np.asarray(surveyData['name'].values.tolist())

# load numpy array of tiled PGP data 
pgp = preprocessing.scale(np.load("/data-sdd/tiling/hiq.218/hiq-pgp").astype('double'))


# In[10]:

# load numpy array of names and keep only the huID
pgpNames = np.load("names")
pgpNames = map(lambda name: name[:8], pgpNames)

# simple lambda function to return if the input is a string
isstr = lambda val: isinstance(val, str)


# In[11]:

eye_color = collections.namedtuple("EyeColor", ['left', 'right'])

# lookup a name in the survey data and return a tuple of the eye colors
def getData(name, surveyData, excludeHazel=False):
    for index, row in surveyData.iterrows():
        if row['name'] == name:
            if not excludeHazel:
                return eye_color(row['left'], row['right'])
            else:
                if isstr(row['left_desc']) and isstr(row['right_desc']):
                    if 'azel' in row['left_desc'] or 'azel' in row['right_desc']:
                        return None
                return eye_color(row['left'], row['right'])


# In[12]:

# list of tuples for index and name with eye color data (idx, name)
nameEyeMap = []
namePair = collections.namedtuple("NamePair", ['index', 'name'])

# dictionary of left and right eye colors with respective name, i.e., {"huID": 12}
leftEyeMap = {}
rightEyeMap = {}

existingNames = []

# loop through pgpNames and add eye color to maps, making sure not to add the same name twice
for i, name in enumerate(pgpNames):
    if name in surveyNames and name not in existingNames:
        existingNames.append(name)
        eyeData = getData(name, surveyData, excludeHazel=True)
        if eyeData == None:
            pass
        elif isstr(eyeData.left) and isstr(eyeData.right):
            nameEyeMap.append(namePair(i, name))
            leftEyeMap[name] = eyeData.left
            rightEyeMap[name] = eyeData.right

# create lists containing the known eye color names and the unknown eye colors.
nameIndices, correspondingNames = [], []
for pair in nameEyeMap:
    nameIndices.append(pair.index)
    correspondingNames.append(pair.name)
knownData = pgp[nameIndices]
unknownData = np.delete(pgp, nameIndices, axis=0)


# In[ ]:

# convert dictionaries to lists 
leftEyeNameList = []
rightEyeNameList = []
# nametuple looks like (index, name)
for _, name in nameEyeMap:
    if isstr(leftEyeMap[name]):
        leftEyeNameList.append(leftEyeMap[name])
    if isstr(rightEyeMap[name]):
        rightEyeNameList.append(rightEyeMap[name])

blueOrNot = lambda color: 0 if int(color) > 13 else 1
leftEyeNameList = map(blueOrNot, leftEyeNameList)


# In[ ]:

# create histogram of blue/not blue. TODO: make labels for graph
plt.hist(leftEyeNameList)
plt.ylabel("Number of Participants")
plt.xlabel("Eye Color")
plt.show()


# In[ ]:

# dump the classifier for analysis
#from sklearn.externals import joblib
#svc_test = LinearSVC(penalty='l1', class_weight='balanced', 
#                     C=.06, dual=False, verbose=1, max_iter=2500)
#svc_test.fit(knownData, leftEyeNameList)
#score = svc_test.score(knownData,leftEyeNameList)
#print(score)

#n = 10
#scores = cross_val_score(svc_test, knownData, leftEyeNameList, cv=n)
#print("Accuracy 10-fold: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:

#joblib.dump(svc_test, "svc_without_hazel.pkl")


# In[ ]:


svc_test = SGDClassifier(penalty='l1', class_weight='balanced', 
                     alpha=.25, verbose=1, n_iter=120000,
                     loss='hinge')

svc_test.fit(knownData, leftEyeNameList)

score = svc_test.score(knownData,leftEyeNameList)
print(score)
