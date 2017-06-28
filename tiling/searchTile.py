# searches for a tile path given its location
# note: requires linux for system 'cat' command.

import numpy as np
import sys, os
import subprocess

coefPaths = np.load("./hiq-pgp-info")
tile_path = np.trunc(coefPaths/(16**5))
tile_step = np.trunc((coefPaths - tile_path*16**5)/2)
tile_phase = np.trunc((coefPaths- tile_path*16**5 - 2*tile_step))
vhex = np.vectorize(hex)
vectorizedPath = vhex(tile_path.astype('int'))
vectorizedStep = vhex(tile_step.astype('int'))
    
def tileSearch(arg):
    vecpath = str(vectorizedPath[int(arg)])
    vecpath = vecpath[2:].zfill(4)
    proc = subprocess.check_output("cat ./assembly.00.hg19.fw.fwi | grep :" + vecpath, shell=True)
    return proc
