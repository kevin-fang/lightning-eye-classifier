#!/usr/bin/env python

import subprocess, argparse
import numpy as np
from subprocess import CalledProcessError

# set up argument parsing
parser = argparse.ArgumentParser(description="From an index of a tile, return the tile name, variants, and/or base pair locations")
parser.add_argument('-i', '--index', type=int, help="an index of the tile", required=True)
parser.add_argument('-l', '--get-location', type=int, nargs='?', default=False, help="whether to get tile location (requires cat, grep, and assembly.00.hg19.fw.fwi)")
parser.add_argument('-v', '--get-variants', type=int, nargs='?', default=False, help="whether to get tile variants (a/t/c/g) (requires zgrep and the keep collection with *.sglf.gz)")
parser.add_argument('-b', '--get-base-pairs', type=int, nargs='?', default=False, help="whether to get base pair locations (requires bgzip and assembly.00.hg19.fw.gz)")
parser.add_argument('--assembly-gz', type=str, nargs='?', default=None, help="location of assembly.00.hg19.fw.gz")
parser.add_argument('--keep', type=str, nargs='?', default=None, help="location of keep collection with *.sglf.gz")
parser.add_argument('--assembly-fwi', type=str, nargs='?', default=None, help="location of assembly.00.hg19.fw.fwi")
args = parser.parse_args()
print args

# set None values to true for easier if statements
if args.get_location == None: 
    assert(args.assembly_fwi != None)
    args.get_location = True
if args.get_variants == None: 
    assert(args.keep != None)
    args.get_variants = True
if args.get_base_pairs == None: 
    assert(args.assembly_gz != None)
    args.get_base_pairs = True

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
        proc = subprocess.check_output("cat " + args.assembly_fwi + " | grep :" + vecpath, shell=True)
        return proc
    except CalledProcessError as e:
        return "Assembly index file not found or `cat` command not available. Continuing..."

# get the location of a tile
def getTileLocation(raw_tile_data):
    split_raw = raw_tile_data.split('\t')
    begin = int(split_raw[2])
    sequence = int(split_raw[1])
    hexVal = split_raw[0].split(':')[2]
    cmdToRun = "bgzip -c -b %d -s %d -d %s | grep -B1 \"%s\s\"" % (begin, sequence, args.assembly_gz, hexVal)
    try:
        subprocess.call("bgzip -r " + args.assembly_gz, shell=True)
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
        print subprocess.check_output("zgrep %s.00.%s %s/%s.sglf.gz" % (tilePath, tileStep, args.keep, tilePath), shell=True) 
    except CalledProcessError:
        print "Collection not found or `zgrep` command not available. Finishing..."
