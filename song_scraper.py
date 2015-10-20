# coding: utf-8

from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib2
import time
import random
import os
import shutil

baseURL = "http://www.azlyrics.com/"
folderName = 'songs'
maxCount = 200
# songCount = 0
# artistCount = 0

START = 0 # start at this file
END = 1
NUM_ARTISTS = 158 # max number

# make folder for song text files
if not os.path.exists(folderName):
	os.mkdir(folderName)

for i in range(START, min(NUM_ARTISTS + 1, END)):
	artists = open(os.path.join('artists', 'artists' + str(i) + '.txt'), 'r')

	textPath = os.path.join(folderName, 'songs' + str(i) + '.txt')
	if os.path.exists(textPath):
		os.remove(textPath)

	songs = open(textPath, 'a')

	# for each artist, gather list of songs
	for line in artists:
		artistName = line.split(' <//> ')[0].title()
		temp = artistName
		if ',' in artistName and not artistName == "Chunk! No, Captain Chunk!":
			artistName = artistName.split(', ')[1] + " " + artistName.split(', ')[0]
			# print temp, "||", artistName
		artistURL = line.split(' <//> ')[1]

		page = urllib2.urlopen(baseURL + artistURL)
		soup = BeautifulSoup(page, 'html.parser')

		for link in soup.find_all('a', { 'target' : "_blank" }):
			if not link.get_text() == None and '../lyrics' in link.get('href'):
				# if not songCount / maxCount == (songCount - 1) / maxCount:
				# 	songs = open(folderName + '/songs' + str(songCount / maxCount) + '.txt', 'a')

				songs.write(artistName + " <//> " + link.get_text().encode('utf8') + " <//> " + link.get('href').encode('utf8') + '\n')
				
				# if not songCount / maxCount == (songCount + 1) / maxCount:
				# 	songs.close()
				# songCount += 1

				# print link.get_text(), link.get('href')

		pause = random.uniform(5, 9)
		print "Finished", artistName, '|| pausing for', pause
		time.sleep(pause)

	songs.close()
	print "Done with file", textPath

print 'Finished scraping!'