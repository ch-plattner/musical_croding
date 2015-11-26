# coding: utf-8

from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib2
import time
import random
import os
import shutil
import sys

baseURL = "http://www.azlyrics.com/"

# Same comment as in artists_scraper.py and divide_artists.py. This gets the root
# path of our git repo.
REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')
folderName = REPO_ROOT + '/Data/lyrics'

# make folder for song text files
if not os.path.exists(folderName):
	os.mkdir(folderName)

if len(sys.argv) <= 1:
	print "Must include name as argument."
	exit(1)

name = sys.argv[1]
songs = open(os.path.join(REPO_ROOT, 'Data', name + '.txt'), 'r')

# after random number of songs, wait a longer period of time
counter = random.uniform(10, 15)

# for each artist, gather list of songs
for line in songs:
	artistName, songName, url = line.split(' <//> ')

	artistFolder = os.path.join(folderName, artistName)
	if not os.path.exists(artistFolder):
		os.mkdir(artistFolder)

	textPath = os.path.join(artistFolder, artistName + ' || ' + songName + '.txt')
	if os.path.exists(textPath):
		os.remove(textPath)

	# Open file for lyrics
	lyrics = open(textPath, 'a')

	url = url[3::]
	print url
	page = urllib2.urlopen(baseURL + url)
	soup = BeautifulSoup(page, 'html.parser')

	# Get all lyrics and print to lyrics file
	for div in soup.findAll('div', { "class" : "lyricsh" }):
		startDiv = div
	divs = soup.findAll('div')
	for i, div in enumerate(divs):
		if div == startDiv:
			lyrics.write(divs[i + 2].get_text().encode('utf8'))
			break

	lyrics.close()

	# Pause after finishing
	pause = random.uniform(7, 13)
	print "Finished", artistName, ':', songName, '|| pausing for', pause
	time.sleep(pause)

	# Every 10-15 songs, longer pause
	counter -= 1
	if counter <= 0:
		pause = random.uniform(60, 90)
		print "Long pause: ", pause
		time.sleep(pause)

		counter = random.uniform(10, 15)

print 'Finished scraping!'