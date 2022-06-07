import os
from os import listdir, walk
from os.path import isfile, join
import json
import sys

def assemble_files(path):
    filenames = next(walk(path), (None, None, []))[2]
    return filenames

def constructGCC(files, out):
    cmd = "gcc  "
    for file in files:
        if file[-2:] == ".c":
            cmd += file + " "
    cmd += "-o " + out
    return cmd

def proC0(data):
    paths = data['sources'] # all paths
    files = []
    for p in paths:
        #files = files + assemble_files(p)
        for fl in assemble_files(p): # go over files
            n = p + fl # add path
            files.append(n) # append to files[]

    print("> Compiler: GCC")
    gcc = constructGCC(files, data['out']['path'] + data['out']['name'])
    print("> " + gcc)
    os.system(gcc)
    print("")

versions = {
    0: proC0
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append('proC.json')

    with open(sys.argv[1], 'r') as f: # open proC file
        data = json.load(f) # load json
    versions[data['version']](data)
    