# coding: utf-8

import os
import shutil
import random

# names = ['charissa', 'owen', 'emily']

folderName = 'songs'

# Get the root path of this repo. Allows you to open the artist and lyrics
# data more safely, now that they've been reorganized into different dirs.
REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')
DATA_ROOT = os.path.join(REPO_ROOT, 'Data')

charissa = open(os.path.join(DATA_ROOT, 'charissa.txt'), 'a')
owen = open(os.path.join(DATA_ROOT, 'owen.txt'), 'a')
emily = open(os.path.join(DATA_ROOT, 'emily.txt'), 'a')

files = [charissa, owen, emily]

songList = []

for fileName in os.listdir(os.path.join(DATA_ROOT, folderName)):
	songList.extend([line for line in open(os.path.join(DATA_ROOT, folderName, fileName))])

random.shuffle(songList)

for song in songList:
	num = random.randint(0, 2)
	files[num].write(song)

charissa.close()
owen.close()
emily.close()