# Kevin Fang, Curoverse 2017
# searches for a tile path given its location
# note: requires unix for system 'cat' command.

import numpy as np
import subprocess
import re

print "Loading tile libraries.."
# load the coefficient paths from pgp data and generate tile path, step, and phase.
coefPaths = np.load("../tile-searcher/tiling-files/hiq-pgp-info")
tile_path = np.trunc(coefPaths/(16**5))
tile_step = np.trunc((coefPaths - tile_path*16**5)/2)
tile_phase = np.trunc((coefPaths - tile_path*16**5 - 2*tile_step))

# generate vectorized path, step, and phase
vhex = np.vectorize(hex)
vectorizedPath = vhex(tile_path.astype('int'))
vectorizedStep = vhex(tile_step.astype('int'))
vectorizedPhase = vhex(tile_phase.astype('int'))

# search for a tile
def tileSearch(arg):
    vecpath = str(vectorizedPath[int(arg)])
    vecpath = vecpath[2:].zfill(4)
    proc = subprocess.check_output("cat ../tile-searcher/tiling-files/assembly.00.hg19.fw.fwi | grep :" + vecpath, shell=True)
    return proc

# get the location of a tile
def getTileLocation(raw_tile_data):
    split_raw = raw_tile_data.split('\t')
    begin = int(split_raw[2])
    sequence = int(split_raw[1])
    hexVal = split_raw[0].split(':')[2]
    cmdToRun = "bgzip -c -b %d -s %d -d ../tile-searcher/tiling-files/assembly.00.hg19.fw.gz | grep -B1 \"%s\s\"" % (begin, sequence, hexVal)
    return subprocess.check_output(cmdToRun, shell=True)

def getTileInfo(index):
    print "Tile Path:", vectorizedPath[index]
    print "Tile Step", vectorizedStep[index]
    print "Tile Phase:", vectorizedPhase[index], "\n"
    tile = tileSearch(index)
    print tile
    print getTileLocation(tile)

# load generated coefficients (sorted by weight)
coefs = np.load("coefs.pkl")
print "Results:\n"

# search for the specific tile location from the coefficients
tileLocations = []
for item in coefs:
    tile = tileSearch(item)
    print tile, item, '\n'
    tileLocations.append(tile)

# get the location of the tile with the highest coefficient
print getTileLocation(tileLocations[0])
