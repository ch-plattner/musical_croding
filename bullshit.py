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

songs = open(os.path.join(REPO_ROOT, 'Data', 'lul.txt'), 'r')
backslash = '\\'

for line in songs:
    com0 = line
    com1 = com0.replace(" ", backslash + " ")
    com2 = com1.replace("'", backslash + "'")
    com3 = com2.replace("|", backslash + "|")
    com4 = com3.replace("(", backslash + "(")
    com5 = com4.replace(")", backslash + ")")
    command = com5
    
    os.system("git checkout --ours " + command)
