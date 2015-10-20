# coding: utf-8

import os
import shutil

folderName = 'artists'
artistsShuffle = open('artists_shuffle.txt', 'r')
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