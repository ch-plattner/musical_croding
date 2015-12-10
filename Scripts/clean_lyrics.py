# Takes a single argument that is a path to the folder of songs that need to be cleaned;
# Outputs the cleaned files to a folder called "output" in the same directory.
# Applies the same conventions as SongParser so that the syntax matches generated songs
# in capitalization and punctuation.

# coding: utf-8

import os
import shutil
import sys

if len(sys.argv) <= 1:
	print "Must include folder path as argument."
	exit(1)

folder_path = sys.argv[1]
output_name = 'output'
output_path = os.path.join(folder_path, output_name)

if not os.path.exists(output_path):
	os.mkdir(output_path)

count = 0
for file_name in os.listdir(folder_path):
	if os.path.isfile(os.path.join(folder_path, file_name)):
		artist_name = file_name.split(' || ')[0]
		song_file = open(os.path.join(folder_path, file_name), 'r')
		output_file = open(os.path.join(output_path, artist_name + '-' + str(count) + '.txt'), 'w')
		line = song_file.readline()
		while line != "":
			if not ("azlyrics.com" in line or "chorus" in line or "Chorus" in line): 
				sanitary = line.translate(None, "`~!@#$%^&*()_+=[]\\{}|;:\",./<>?\n\r\a\b\f\t\v").lower()
				output_file.write(sanitary + '\n')
			line = song_file.readline()
		song_file.close()
		output_file.close()
		count += 1