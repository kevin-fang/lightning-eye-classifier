# Kevin Fang, Curoverse 2017

from sklearn.svm import LinearSVC
from sklearn import preprocessing
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import collections

# change for whether to exclude or include hazel
excludeHazel = True

# file name of saved classifier
fileName = 'svc.pkl'

# read names that have provided survey eye color data
columns = ['name', 'timestamp', 'id', 'blood_type', 'height', 'weight', 'hw_comments', 'left', 'right', 'left_desc', 'right_desc', 'eye_comments', 'hair', 'hair_desc', 'hair_comments', 'misc', 'handedness']

# pgp eye color data from survey
print "Loading data..."
surveyData = pd.read_csv("../eye_color_data/PGP-Survey.csv", names=columns, na_values=['nan', '', 'NaN'])

# names of the pgp participants
surveyNames = np.asarray(surveyData['name'].values.tolist())

# load numpy array of tiled PGP data 
pgp = preprocessing.scale(np.load("../hiq-pgp").astype('double'))

# load numpy array of names and keep only the huID
pgpNames = np.load("../names")
pgpNames = map(lambda name: name[:8], pgpNames)

# simple lambda function to return if the input is a string
isstr = lambda val: isinstance(val, str)

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
        # change `excludeHazel=True` to include hazel in the training/testing data.
        eyeData = getData(name, surveyData, excludeHazel=excludeHazel)
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

# convert dictionaries to lists 
leftEyeList = []
rightEyeList = []
# nametuple looks like (index, name)
for _, name in nameEyeMap:
    if isstr(leftEyeMap[name]):
        leftEyeList.append(leftEyeMap[name])
    if isstr(rightEyeMap[name]):
        rightEyeList.append(rightEyeMap[name])

blueOrNot = lambda color: 0 if int(color) > 13 else 1
leftEyeList = map(blueOrNot, leftEyeList)

# dump the classifier for analysis
from sklearn.externals import joblib
print "Training classifier..."
svc_test = LinearSVC(penalty='l1', class_weight='balanced', 
                     C=.06, dual=False, verbose=0, max_iter=2500)
svc_test.fit(knownData, leftEyeList)

print "Saving classifier in", fileName
joblib.dump(svc_test, fileName)