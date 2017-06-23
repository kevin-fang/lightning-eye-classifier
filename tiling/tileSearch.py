#!/usr/bin/env python
# Usage: find the location of the tile of a genome. 
# Example command (search for tile position 1949505):
# ./tileSearch.py 1949505

import numpy as np
import sys, os

# load numpy array and set tile path, step, and phase arrays
coefPaths = np.load("./hiq-pgp-info")
tile_path = np.trunc(coefPaths / (16 ** 5))
tile_step = np.trunc((coefPaths - tile_path * 16 ** 5) / 2)
tile_phase = np.trunc((coefPaths - tile_path* 16 ** 5 - 2 * tile_step))
# allow the hex function to fectorize
vhex = np.vectorize(hex)

# retrieve the tile path in hex
vectorizedPath = vhex(tile_path.astype('int'))
vecpath = str(vectorizedPath[int(sys.argv[1])])
print "tile path: " + vecpath 

# retrieve the tile step in hex
vectorizedStep = vhex(tile_step.astype('int'))
print "tile step: " + str(vectorizedStep[int(sys.argv[1])])

# search for the vector path in the tile assembly file
vecpath = vecpath[2:]
vecpath = vecpath.zfill(4)
os.system("cat assembly.00.hg19.fw.fwi | grep " + vecpath) 
