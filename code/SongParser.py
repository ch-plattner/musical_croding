import os, sys
from os import path
from collections import Counter

# Class: SongParser
# -----------------
# ???
#
class SongParser:
    # Constructor: SongParser
    # -----------------------
    # Takes in an optional argument, |song|, of the form
    # "<artist> || <song_name>.txt"
    # the same as each scraped lyrics file's name.
    # If song is provided, then parsing and model creation
    # are automatically initiated. It is up to the user to
    # ensure the optional arg is correctly formatted. 
    def __init__(self, song = None):
        self.root = os.popen("git rev-parse --show-toplevel").read().strip('\n') + "/Data/lyrics"
        # BELOW IS UNTESTED
        if song != None:
            artistname = song.split('||')[0].strip(' ')
            self.parse_song(self.root + '/' + artistname + '/' + song)
            self.create_unigram_model()
            self.create_bigram_model()
            self.create_trigram_model()


    # Function: parse_song
    # --------------------
    # Take the raw lyrics and clean it up. Remove noise, and
    # return a list of song lines stored in |self.lyrics|. 
    def parse_song(self, raw_lyrics_path):
        lyrics_file = open(raw_lyrics_path, 'r')    # this function is beautiful it adds backslashes for you
        self.lyrics = []
         
        # Remove symbols not useful to our project, and lowercase everything.
        # Apostrophes may be appropriate, but are removed for standardization. Some artists use them, some don't.
        line = lyrics_file.readline()
        while (line != ""):
            if not ("azlyrics.com" in line or "chorus" in line or "Chorus" in line): 
                sanitary = line.translate(None, "`~!@#$%^&*()_+=[]\\{}|;:\",./<>?\n").lower()
                if sanitary != "":
                    self.lyrics.append(sanitary)
            line = lyrics_file.readline()
            
    # -------------------------------------
    # Creating Markov models
    # ======================
    # Creates unigram, bigram, and trigram
    # models from the list of song lines
    # the SongParser extracted.
    #
    # THIS IS STILL UNTESTED
    # -------------------------------------

# Note, it might be a good idea to build our own util.py with stuff like WeightedRandomChoice

    def create_unigram_model(self):
        model = Counter()
        if len(self.lyrics) == 0:
            raise Exception("No lyrics exist!")

        for line in self.lyrics:
            model.update(line.split())
        self.unigram_model = model

    def create_bigram_model(self):
        model = Counter()
        if len(self.lyrics) == 0:
            raise Exception("No lyrics exist!")

        for line in self.lyrics:
            words = line.split()
            model.update([(words[i], words[i+1]) for i in range(len(words)-1)])
        self.bigram_model = model

    def create_trigram_model(self):
        model = Counter()
        if len(self.lyrics) == 0:
            raise Exception("No lyrics exist!")

        for line in self.lyrics:
            words = line.split()
            model.update([(words[i], words[i+1], words[i+2]) for i in range(len(words)-2)])
        self.trigram_model = model


##########################################################
#
#   TEST CODE
# -------------
# If you're not concerned with testing the SongParser
# class, you can stop here. Nothing below is of interest.
#
##########################################################
if len(sys.argv) <= 1:
    sys.exit(0)

sp = SongParser()
if "parse" in sys.argv:
    sp.parse_song(sp.root + "/Owl City/Owl City || Dementia.txt")
    print "\n"
    for line in sp.lyrics:
        print line

    sp.parse_song(sp.root + "/Bastille/Bastille || Laughter Lines.txt")
    print "\n"
    for line in sp.lyrics:
        print line

    sp.parse_song(sp.root + "/Eminem/Eminem || Kill You.txt")
    print "\n"
    for line in sp.lyrics:
        print line

if "model" in sys.argv:

if "cons" in sys.argv:
