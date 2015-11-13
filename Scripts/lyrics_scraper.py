# coding: utf-8

from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib2
import time
import random
import os
import shutil

baseURL = "http://www.azlyrics.com/"

# Same comment as in artists_scraper.py and divide_artists.py. This gets the root
# path of our git repo.
REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')
folderName = REPO_ROOT + 'Data/lyrics'
maxCount = 200

START = -1 # start at this file
END = 0
# ????????? Why is the max number of songs 158? Was this specifically for TSwift? - Owen 11.13.15
NUM_SONGS = 158 # max number

# make folder for song text files
if not os.path.exists(folderName):
	os.mkdir(folderName)

for i in range(START, min(NUM_SONGS + 1, END)):
	songs = open(os.path.join('songs', 'songs' + str(i) + '.txt'), 'r')

	songsList = [line for line in songs]
	random.shuffle(songsList)

	for line in songsList:
		artistName, songName, url = line.split(' <//> ')

		textPath = os.path.join(folderName, 'lyrics - ' + artistName + ' - ' + songName + '.txt')
		if os.path.exists(textPath):
			os.remove(textPath)

		lyrics = open(textPath, 'a')

		url = url[3::]
		print url
		page = urllib2.urlopen(baseURL + url)
		soup = BeautifulSoup(page, 'html.parser')

		for div in soup.findAll('div', { "class" : "lyricsh" }):
			startDiv = div
		divs = soup.findAll('div')
		for i, div in enumerate(divs):
			if div == startDiv:
				lyrics.write(divs[i + 2].get_text().encode('utf8'))
				break

		lyrics.close()
		pause = random.uniform(5, 15)
		print "Finished", artistName, songName, '|| pausing for', pause
		time.sleep(pause)

	songs.close()
	print "Done with artist", artistName

print 'Finished scraping!'
