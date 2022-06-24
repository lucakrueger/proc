import os
from os import listdir, walk
from os.path import isfile, join
import json
import sys
from venv import create

def assemble_files(path):
    filenames = next(walk(path), (None, None, []))[2]
    return filenames

# VERSION 0
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

# VERSION 1
typeidents = {
    "static": "-c",
    "shared": "-dynamiclib",
    "exec": ""
}

def create_gcc(files, out, flags, type):
    filenames = ""
    for file in files:
        if file[-2:] == ".c":
            filenames += file + " "
    
    flagnames = ""
    for flag in flags:
        flagnames += flag + " "
    
    typeident = typeidents[type]

    return "gcc {typeident} {filenames}{flags}-o {out}".format(typeident = typeident, filenames = filenames, flags = flagnames, out = out)

def files_from_paths(paths):
    files = []
    for p in paths:
        if p[-1:] != "/":
            p += "/"
        for fl in assemble_files(p):
            n = p + fl # add path
            files.append(n)
    return files

def run_scripts(scripts):
    for script in scripts:
        print("> {script}".format(script = script))
        os.system(script)

def process_target(data):
    if 'scripts' in data:
        run_scripts(data['scripts'])

    paths = data['sources']
    files = files_from_paths(paths)
    print("> Compiler: GCC")

    targetdic = {
        "path": "./",
        "type": "exec",
        "flags": []
    }

    if 'target' in data:
        targetdic = data['target']

    flags = []
    if 'flags' in targetdic:
        flags = targetdic['flags']
    
    outtype = "exec"
    if 'type' in targetdic:
        outtype =targetdic['type']

    outfile = targetdic['path']
    if outfile[-1:] != "/":
        outfile += "/"
    outfile += data['name']
        

    gcc = create_gcc(files, outfile, flags, outtype)
    print("> {gcc}".format(gcc = gcc))
    os.system(gcc)
    print("")

def proc1(data):
    for target in data['targets']:
        process_target(target)

versions = {
    0: proC0,
    1: proc1
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append('proc.json')

    with open(sys.argv[1], 'r') as f: # open proC file
        data = json.load(f) # load json
    versions[data['version']](data)
    