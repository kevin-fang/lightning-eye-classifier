# Kevin Fang, Curoverse 2017

import numpy as np
import pandas as pd
import math
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.externals import joblib

# load the saved support vector classifier
svc_test = joblib.load("svc.pkl")

# retrieve all the nonzero coefficients and zip them with their respective indices
nonzeroes = np.nonzero(svc_test.coef_[0])[0]
coefs = zip(nonzeroes, abs(svc_test.coef_[0][nonzeroes]))

# sort the coefficients by their value, instead of index
coefs.sort(key = lambda x: x[1], reverse=True)

print "The classifier produced the following coefficients:"
for coef in coefs:
    print "Index:", coef[0], "weight:", coef[1]

# save just the coefficient values
firstCoefs = [coef[0] for coef in coefs]
indices = np.asarray(firstCoefs)

# dump the coefficients for tiling analysis
indices.dump("coefs.pkl")
print "Coefficients saved in coefs.pkl"
