# coding: utf-8

from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib2
import time
import random
import os

baseURL = "http://www.azlyrics.com/"

# Get the root path of this git repo. Allows you to open the artist and lyrics
# data more safely, now that they've been reorganized into different dirs.
REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')
DATA_ROOT = REPO_ROOT + '/Data'

f = open(DATA_ROOT + '/artists.txt', 'w')

alphabet = list(ascii_lowercase)
random.shuffle(alphabet)

for c in alphabet:
	url = baseURL + c + ".html"
	print url
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')

	for div in soup.find_all('div'):
		if 'artist-col' in div['class']:
			for link in div.find_all('a'):
				# print link.get_text()
				f.write(link.get_text().encode('utf8') + " <//> " + link.get('href').encode('utf8') + '\n')

	pause = random.uniform(5, 10)
	print "Finished", c, 'pausing for', pause
	time.sleep(pause)
print "Finished scraping."
