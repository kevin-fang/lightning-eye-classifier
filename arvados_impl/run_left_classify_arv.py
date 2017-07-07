#!/usr/bin/env python
# Kevin Fang, Curoverse, 2017
from sklearn.svm import LinearSVC
from sklearn import preprocessing
import numpy as np
import pandas as pd
import subprocess
import collections

'''

dependencies: hiq-pgp, names, hiq-pgp-info, assembly.00.hg19.fw.fwi, assembly.00.fg19.fw.gz, assembly.00.hg19.fw.gz.gzi
descriptions:
  hiq-pgp: numpy array of high quality tiles
  names: numpy array of names corresponding to high quality tiles
  hiq-pgp-info: coefficient paths for tiled data
  assembly.00.hg19.fw.gz: gzipped fw assembly file
  assembly.00.hg19.fw.fwi: indices for assembly fw file
usage: run_left_classify_arv.py <hiq-pgp> <names> <hiq-pgp-info> <assembly..gz> <assembly...fwi> <assembly...gzi> 

'''
from sys import argv, exit
if len(argv) != 7:
    print "usage: run_left_classify_arv.py <hiq-pgp> <names> <hiq-pgp-info> <assembly..gz> <assembly...fwi> <pgp-survey>"
    exit(1) 

hiqPgp = argv[1]
names = argv[2]
hiqPgpInfo = argv[3]
assemblyGz = argv[4]
assemblyFwi = argv[5]
pgpSurvey = argv[6]

print "Loading names, survey, and tile data..."
# pgp eye color data from survey
## read names that have provided survey eye color data
columns = ['name', 'timestamp', 'id', 'blood_type', 'height', 'weight', 'hw_comments', 'left', 'right', 'left_desc', 'right_desc', 'eye_comments', 'hair', 'hair_desc', 'hair_comments', 'misc', 'handedness']

# pgp eye color data from survey
surveyData = pd.read_csv(pgpSurvey, names=columns, na_values=['nan', '', 'NaN'])

# names of the pgp participants
surveyNames = np.asarray(surveyData['name'].values.tolist())

# load numpy array of tiled PGP data 
pgp = preprocessing.scale(np.load(hiqPgp).astype('double'))

# load numpy array of names and keep only the huID
pgpNames = np.load(names)
pgpNames = map(lambda name: name[:8], pgpNames)

# simple lambda function to return if the input is a string
isstr = lambda val: isinstance(val, str)

print "Finished loading data.",
eye_color = collections.namedtuple("EyeColor", ['left', 'right'])

# lookup a name in the survey data and return a tuple of the eye colors
def getAllData(name, surveyData):
    for index, row in surveyData.iterrows():
        if row['name'] == name:
            return eye_color(row['left'], row['right'])
        
# lookup a name in the survey data and return a tuple of the eye colors, excluding hazel
def getDataNoHazel(name, surveyData):
    for index, row in surveyData.iterrows():
        if row['name'] == name:
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
        eyeData = getDataNoHazel(name, surveyData)
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
leftEyeNameList = []
rightEyeNameList = []
# nametuple looks like (index, name)
for _, name in nameEyeMap:
    if isstr(leftEyeMap[name]):
        leftEyeNameList.append(leftEyeMap[name])
    if isstr(rightEyeMap[name]):
        rightEyeNameList.append(rightEyeMap[name])

blueOrNot = lambda name: 0 if int(name) > 13 else 1
leftEyeNameList = map(blueOrNot, leftEyeNameList)
        
print "Finished processing data.",

print "Running support vector classifier..."
svc_test = LinearSVC(penalty='l1', class_weight='balanced', 
                     C=.06, dual=False, max_iter=2500)
svc_test.fit(knownData, leftEyeNameList)

print "Classifier done. Retrieving coefficients..."
# retrieve all the nonzero coefficients and zip them with their respective indices
nonzeroes = np.nonzero(svc_test.coef_[0])[0]
coefs = zip(nonzeroes, svc_test.coef_[0][nonzeroes])

# sort the coefficients by their value, instead of index
coefs.sort(key = lambda x: x[1], reverse=True)

# save just the coefficient values
firstCoefs = [coef[0] for coef in coefs]
indices = np.asarray(firstCoefs)
print "Highest coefficient:", str(coefs[0][1]), "Index:", coefs[0][0]

# searches for a tile path given its location
# note: requires unix for system 'cat' command.
print "Coefficients loaded. Searching tiles..."
# load the coefficient paths from pgp data and generate tile path, step, and phase.
coefPaths = np.load(hiqPgpInfo)
tile_path = np.trunc(coefPaths/(16**5))
tile_step = np.trunc((coefPaths - tile_path * 16 ** 5) / 2)
tile_phase = np.trunc((coefPaths - tile_path* 16 ** 5 - 2 * tile_step))
vhex = np.vectorize(hex)
vectorizedPath = vhex(tile_path.astype('int'))
vectorizedStep = vhex(tile_step.astype('int'))
subprocess.call("bgzip -r " + assemblyGz, shell=True)

# search for a tile
def tileSearch(arg):
    vecpath = str(vectorizedPath[int(arg)])
    vecpath = vecpath[2:].zfill(4)
    proc = subprocess.check_output("cat " + assemblyFwi + " | grep :" + vecpath, shell=True)
    return proc

# get the location of a tile
def getTileLocation(raw_tile_data):
    split_raw = raw_tile_data.split('\t')
    begin = int(split_raw[2])
    sequence = int(split_raw[1])
    hexVal = split_raw[0].split(':')[2]
    cmdToRun = "bgzip -c -b %d -s %d -d %s | grep -B1 \"%s\s\"" % (begin, sequence, assemblyGz, hexVal)
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
