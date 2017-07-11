#!/usr/bin/env python

import subprocess, argparse
import numpy as np
from subprocess import CalledProcessError

# set up argument parsing
parser = argparse.ArgumentParser(description="Get base pairs from tile variant or location")
parser.add_argument('-i', '--index', type=int, help="an index of the tile", required=True)
parser.add_argument('-l', '--get-location', type=int, nargs='?', default=False)
parser.add_argument('-v', '--get-variants', type=int, nargs='?', default=False)
parser.add_argument('-b', '--get-base-pairs', type=int, nargs='?', default=False)
args = parser.parse_args()

# set None values to true for easier if statements
if args.get_location == None: args.get_location = True
if args.get_variants == None: args.get_variants = True
if args.get_base_pairs == None: args.get_base_pairs = True

# set up information needed for tile search
coefPaths = np.load('hiq-pgp-info')
tile_path = np.trunc(coefPaths/(16**5))
tile_step = np.trunc((coefPaths - tile_path*16**5)/2)
tile_phase = np.trunc((coefPaths - tile_path*16**5 - 2*tile_step))
vhex = np.vectorize(hex)
vectorizedPath = vhex(tile_path.astype('int'))
vectorizedStep = vhex(tile_step.astype('int'))
vectorizedPhase = vhex(tile_phase.astype('int'))

# search for a tile
def tileSearch(arg):
    vecpath = str(vectorizedPath[int(arg)])
    vecpath = vecpath[2:].zfill(4)
    try:
        proc = subprocess.check_output("cat ./assembly.00.hg19.fw.fwi | grep :" + vecpath, shell=True)
    except CalledProcessError as e:
        print "Assembly index file not found or `cat` command not available. Exiting..."
        sys.exit(1)
    return proc

# get the location of a tile
def getTileLocation(raw_tile_data):
    split_raw = raw_tile_data.split('\t')
    begin = int(split_raw[2])
    sequence = int(split_raw[1])
    hexVal = split_raw[0].split(':')[2]
    cmdToRun = "bgzip -c -b %d -s %d -d ./assembly.00.hg19.fw.gz | grep -B1 \"%s\s\"" % (begin, sequence, hexVal)
    try:
        output = subprocess.check_output(cmdToRun, shell=True)
        return output
    except CalledProcessError as e:
        return "bgzip not installed or assembly file (assembly.00.hg19.fw.gz) not found. Continuing...."

# get the tile path, step, and phase and print out if needed
tilePath = vectorizedPath[args.index]
tileStep = vectorizedStep[args.index]
tilePhase = vectorizedPhase[args.index]
tile = tileSearch(args.index)
if (args.get_location):
    print "Tile Path:", tilePath
    print "Tile Step:", tileStep 
    print "Tile Phase:", tilePhase 
    print tile

# print out base pairs if needed
if (args.get_base_pairs):
    print getTileLocation(tile)
print
# print out tiles if needed
tilePath = tilePath[2:].zfill(4)
tileStep = tileStep[2:].zfill(4)
if (args.get_variants):
    try:
        print subprocess.check_output("zgrep %s.00.%s ~/keep/by_id/su92l-4zz18-fkbdz2w6b25ayj3/%s.sglf.gz" % (tilePath, tileStep, tilePath), shell=True) 
    except CalledProcessError:
        print "Collection not found or `zgrep` command not available"
        sys.exit(1)
