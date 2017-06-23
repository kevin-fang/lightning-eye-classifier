import numpy as np
import sys

coefPaths = np.load("./hiq-pgp-info")
tile_path = np.trunc(coefPaths/(16**5))
tile_step = np.trunc((coefPaths - tile_path*16**5)/2)
tile_phase = np.trunc((coefPaths- tile_path*16**5 - 2*tile_step))

vhex = np.vectorize(hex)

vectorizedPath = vhex(tile_path.astype('int'))
vecpath = str(vectorizedPath[int(sys.argv[1])])
print "tile path: " + vecpath 

vectorizedStep = vhex(tile_step.astype('int'))
print "tile step: " + str(vectorizedStep[int(sys.argv[1])])

import os
vecpath = vecpath[2:]
vecpath = vecpath.zfill(4)
os.system("cat assembly.00.hg19.fw.fwi | grep " + vecpath) 
