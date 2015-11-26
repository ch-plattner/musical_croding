# coding: utf-8

import os
import shutil
import sys

if len(sys.argv) <= 1:
	print "Must include file name as argument."
	exit(1)

with open(sys.argv[1], 'r') as f:
	lines = f.read().splitlines()

for line in set(lines):
	print line

f.close()