from sklearn.svm import SVC
import numpy as np
import pandas as pd

columns = ['left', 'right']
data = pd.read_csv("PGP-eyecolor.csv", names=columns)
data.columns = columns
print data.head()
