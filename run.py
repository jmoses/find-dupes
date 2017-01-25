#!/usr/bin/env python

import hashlib
import os
import os.path
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--delete-dupes', dest='delete', action='store_true')

args = parser.parse_args()

cwd = '.'

hashes = defaultdict(list) # dict[hash] => file

def prune_dotted(names):
    for n in list(names):
        if n.startswith('.'):
            names.remove(n)

def hash(f):
    md5 = hashlib.md5()
    with open(f, 'rb') as inp:
        while True:
            data = inp.read(65536)
            if not data:
                break

            md5.update(data)

    return md5.hexdigest()

def handle(_, dirname, names):
    prune_dotted(names)
    
    for f in names:
        full = os.path.join(dirname, f)
        if os.path.isfile(full):
            hashes[hash(full)].append(full)


os.path.walk(cwd, handle, 'foo')


for h in hashes:
    if len(hashes[h]) > 1:
        print "Found duplicate files: \n " + "\n ".join(hashes[h])

        if args.delete:
            for f in hashes[h][1:]:
                print "Deleting " + f
                os.remove(f)
