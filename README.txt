CS 221 Final Project
====================
This README documents some operational basics of our project, and decomposes
the different Python scripts used in our lyrics generator. Our code is inside
|Code|, and data is inside |Data|. 

NOTE: To work properly, these two directories should be on the top level 
of a git repository.

We used libraries numpy, sklearn, nltk, pyenchant.

#############################################

Operation
-----------
The script that encapsulates our lyrics generator's use is 
|generate_lyrics_console.py|. To use this, simply cd into the directory with
the script and run "python generate_lyrics_console.py".

The generator will prompt for an artist name, followed by one of three
themes. Please type the artist name as it appears in the |Data| folder.

#############################################

Data
----------

Not very useful:
emily.txt, owen.txt, charissa.txt   - Used in data scraping. Can safely ignore.
80 songs   - archive of songs removed from data collection.
top-artists.txt   - used in data collection.
files-to-fix.txt   - corrupted titles that we addressed. Can safely ignore.

More useful:
songs    = Contains files of all our artists; names of all their songs are inside.

lyrics   = Contains folders of all our artists; files named after each song are
           inside, containing the entire text of each song's lyrics.
           IMPORTANT: Each song file is named "<artist name> || <song name>.txt",
           and we parse it back in this format.

Dev Set  = Songs set aside for evaluation later in the project.

#############################################

Code
-----------

song_parsing.py      = Functions to explore |Data| and catalog all artists and their
                       songs. A script to take this information and generate
                       |unigrams.txt|, |bigrams.txt|, and |trigrams.txt| which contain
                       the N-gram corpi taken from the union of all artists.

song_cluster.py      = Functions for clustering songs from a given artist into 
                       three clusters.

line_generator.py    = Functions to generate one line of lyrics, as well as parsing
                       |uni/bi/trigrams.txt| back into data.

SongParser.py        = An object that captures all the relevant information
                       about a song.

Artist.py            = An object that captures all the relevant information
                       about an artist. This builds off of |SongParser|.

CreatedSong.py       = An object representing a new song we are generating.
                       Has functions inside to generate and store the song's
                       structure, and then print it out to console.

generate_lyrics_console.py = The interface for the user to play with. Uses all
                       of the code above.

IPYNB_files are miscellaneous files used in creating graphs of our clustering
                       algorithm.

#############################################

Scripts
------------

Code used to collect the artist and song data used in this project.

############################################
############################################
