# coding: utf-8

import os
import shutil

folderName = 'Data/artists'

# Get the root path of this repo. Allows you to open the artist and lyrics
# data more safely, now that they've been reorganized into different dirs.
REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')
DATA_ROOT = REPO_ROOT + '/Data'

artistsShuffle = open(DATA_ROOT + '/artists_shuffle.txt', 'r')

maxCount = 50
count = 0

# make folder for text files
if os.path.exists(folderName):
	shutil.rmtree(folderName)
os.mkdir(folderName)

for line in artistsShuffle:
	if not 'http' in line:
		if not count / maxCount == (count - 1) / maxCount:
			artists = open(folderName + '/artists' + str(count / maxCount) + '.txt', 'a')

		artists.write(line)

		if not count / maxCount == (count + 1) / maxCount:
			artists.close()
		count += 1
