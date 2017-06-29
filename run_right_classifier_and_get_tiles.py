#!/usr/bin/env python
# Kevin Fang, Curoverse, 2017
from sklearn.svm import LinearSVC
from sklearn import preprocessing
import numpy as np
import pandas as pd
import subprocess

print "Loading names, survey, and tile data..."
columns = ['name', 'left', 'right', 'left_desc', 'right_desc']
# load survey data
surveyData = pd.read_csv("./eye_color_data/PGP-eyecolor.csv", names=columns, na_values=['nan', ''])
surveyNames = np.asarray(surveyData['name'].values.tolist())

# load numpy array of names and keep only the huID
pgpNames = np.load("names.npy")
for i in range(len(pgpNames)):
    pgpNames[i] = pgpNames[i][:8]

# load numpy array of tiled PGP data 
pgp = np.load("hiq-pgp.npy")

print "Finished loading data.",
# lookup a name in the survey data and return a tuple of the eye colors
def getData(name, surveyData):
    for index, row in surveyData.iterrows():
        if row['name'] == name:
            return (row['left'], row['right'])

# list of tuples for index and name with eye color data
namePairIndices = []

# dictionary of left and right eye colors with respective name, i.e., {"huID": 12}
nameLeftEyeMap = {}
nameRightEyeMap = {}

existingNames = []

print "Processing..."
# loop through pgpNames and add eye color to maps, making sure not to add the same name twice
for i in range(len(pgpNames)):
    name = pgpNames[i]
    if name in surveyNames and name not in existingNames:
        existingNames.append(name)
        eyeData = getData(name, surveyData)
        namePairIndices.append((i, name))
        nameLeftEyeMap[name] = eyeData[0]
        nameRightEyeMap[name] = eyeData[1]

# create lists containing the known eye color names and the unknown eye colors.
nameIndices = [nameIndex[0] for nameIndex in namePairIndices]
knownData = pgp[nameIndices]
unknownData = np.delete(pgp, nameIndices, axis=0)

# convert dictionaries to lists 
leftEyeNameList = []
rightEyeNameList = []

for nameTuple in namePairIndices:
    leftEyeNameList.append(nameLeftEyeMap[nameTuple[1]])
    rightEyeNameList.append(nameRightEyeMap[nameTuple[1]])

# changes values to only blue/not blue for binary classification
for i in range(len(rightEyeNameList)): 
    if rightEyeNameList[i] > 12:
        rightEyeNameList[i] = 0 # not blue
    else:
        rightEyeNameList[i] = 1 # blue

# scale the data
knownData = preprocessing.scale(knownData.astype('double'))
print "Finished processing data.",

print "Running support vector classifier..."
svc_test = LinearSVC(penalty='l1', class_weight='balanced', 
                     C=.06, dual=False, max_iter=2500)
svc_test.fit(knownData, rightEyeNameList)

print "Classifier done. Retrieving coefficients..."
# retrieve all the nonzero coefficients and zip them with their respective indices
nonzeroes = np.nonzero(svc_test.coef_[0])[0]
coefs = zip(nonzeroes, svc_test.coef_[0][nonzeroes])

# sort the coefficients by their value, instead of index
coefs.sort(key = lambda x: x[1], reverse=True)

# save just the coefficient values
firstCoefs = [coef[0] for coef in coefs]
indices = np.asarray(firstCoefs)
print "Highest coefficient:", str(coefs[0][1]), "Index:",  coefs[0][0]

# searches for a tile path given its location
# note: requires unix for system 'cat' command.
print "Coefficients loaded. Searching tiles..."
# load the coefficient paths from pgp data and generate tile path, step, and phase.
coefPaths = np.load("./tiling/hiq-pgp-info")
tile_path = np.trunc(coefPaths/(16**5))
tile_step = np.trunc((coefPaths - tile_path * 16 ** 5) / 2)
tile_phase = np.trunc((coefPaths - tile_path* 16 ** 5 - 2 * tile_step))
vhex = np.vectorize(hex)
vectorizedPath = vhex(tile_path.astype('int'))
vectorizedStep = vhex(tile_step.astype('int'))

# search for a tile
def tileSearch(arg):
    vecpath = str(vectorizedPath[int(arg)])
    vecpath = vecpath[2:].zfill(4)
    proc = subprocess.check_output("cat ./tiling/assembly.00.hg19.fw.fwi | grep :" + vecpath, shell=True)
    return proc

# get the location of a tile
def getTileLocation(raw_tile_data):
    split_raw = raw_tile_data.split('\t')
    begin = int(split_raw[2])
    sequence = int(split_raw[1])
    hexVal = split_raw[0].split(':')[2]
    cmdToRun = "bgzip -c -b %d -s %d -d ./tiling/assembly.00.hg19.fw.gz | grep -B1 \"%s\s\"" % (begin, sequence, hexVal)
    proc = subprocess.check_output(cmdToRun, shell=True)
    return proc

# search for the specific tile location from the coefficients
tileLocations = []
for item in indices:
    tile = tileSearch(item)
    tileLocations.append(tile)

print "Highest coefficient tile:\n" + tileLocations[0]
print "Corresponding Tile location:"
# get the location of the tile with the highest coefficient
print getTileLocation(tileLocations[0])
