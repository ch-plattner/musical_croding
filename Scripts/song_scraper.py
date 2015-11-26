# coding: utf-8

from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib2
import time
import random
import os
import shutil
import sys

if len(sys.argv) <= 1:
	print "Must include file name as argument."
	exit(1)

baseURL = "http://www.azlyrics.com/"

# Same comment as all the other scripts. This gets the root path of our repo
# because data files and dirs are not in the same place anymore; this is safer.
REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')
folderName = REPO_ROOT + '/Data/songs'

# make folder for song text files
if not os.path.exists(folderName):
	os.mkdir(folderName)

fileName = sys.argv[1]
artists = open(fileName, 'r')

# after random number of songs, wait a longer period of time
counter = random.uniform(10, 15)

# for each artist, gather list of songs
for line in artists:
	artistName = line.split(' <//> ')[0].title()
	artistURL = line.split(' <//> ')[1]

	textPath = os.path.join(folderName, artistName + '.txt')
	if os.path.exists(textPath):
		os.remove(textPath)
	songs = open(textPath, 'a')

	page = urllib2.urlopen(baseURL + artistURL)
	soup = BeautifulSoup(page, 'html.parser')

	for link in soup.find_all('a', { 'target' : "_blank" }):
		if not link.get_text() == None and '../lyrics' in link.get('href'):
			songs.write(artistName + " <//> " + link.get_text().encode('utf8') + " <//> " + link.get('href').encode('utf8') + '\n')
			
	songs.close()

	pause = random.uniform(7, 13)
	print "Finished", artistName, '|| pausing for', pause
	time.sleep(pause)

	counter -= 1
	if counter <= 0:
		pause = random.uniform(60, 90)
		print "Long pause: ", pause
		time.sleep(pause)

		counter = random.uniform(10, 15)

print 'Finished scraping!'
