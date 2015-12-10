import os, sys
from os import path
from collections import Counter
import re

# Class: SongParser
# -----------------
# The object for interacting with an individual song and its lyrics.
# 
# Attributes: |self.
#   root| = the lyrics directory relative to the Git repo, for convenience.
#   name| = the name of the song
#   lyrics| = a list of lines in the song
#   unigrams|,
#   bigrams|,
#   trigrams| = dicts from (uni/bi/trigram) : weight
#   line_lengths| = a list of the length (in words) of each line.
#   num_lines|, duh.
#   word_count| = total # words in song.
#   min_line|,
#   max_line|,
#   mean_line|
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
        if song != None:
            artistname = song.split('||')[0].strip(' ')
            self.parse_song(song)
            self.get_stats()
            self.create_unigram_model()
            self.create_bigram_model()
            self.create_trigram_model()


    # Function: parse_song
    # --------------------
    # Take the raw lyrics and clean it up. Remove noise, and
    # return a list of song lines stored in |self.lyrics|. 
    def parse_song(self, song):
        self.artistname = song.split('||')[0].strip(' ')
        lyrics_file = open(self.root + '/' + self.artistname + '/' + song, 'r')
        self.lyrics = []
        self.name = song
        self.line_lengths = []

        # Remove symbols not useful to our project, and lowercase everything.
        # Apostrophes may be appropriate, so those can stay.
        line = lyrics_file.readline()
        while (line != ""):
            if not ("azlyrics.com" in line or "chorus" in line or "Chorus" in line): 
                sanitary = line.translate(None, "`~!@#$%^&*()_+=[]\\{}|;:\",./<>?\n\r\a\b\f\t\v").lower()
                if sanitary != "":
                    self.lyrics.append(sanitary)
                    self.line_lengths.append(len(re.findall(r'\w+', line))) # Counts number of words in the line
            line = lyrics_file.readline()

    # Function: get_stats
    # --------------------
    # Uses the |self.line_lengths| list from parse_song to calculate stats 
    # such as the total word count, average line length, min/max 
    # line length, and number of lines
    def get_stats(self):
        self.num_lines = len(self.line_lengths)
        self.word_count = sum(self.line_lengths)
        self.min_line = min(self.line_lengths)
        self.max_line = max(self.line_lengths)
        self.mean_line = self.word_count / float(self.num_lines)

            
    # -------------------------------------
    # Creating Markov models
    # ======================
    # Creates unigram, bigram, and trigram
    # models from the list of song lines
    # the SongParser most recently extracted.
    #
    # -------------------------------------

# Note, it might be a good idea to build our own util.py with stuff like WeightedRandomChoice

    def create_unigram_model(self):
        model = Counter()
        if len(self.lyrics) == 0:
            raise Exception("No lyrics exist!")
        for line in self.lyrics:
            model.update(line.split())
        self.unigrams = model

    def create_bigram_model(self):
        model = Counter()
        if len(self.lyrics) == 0:
            raise Exception("No lyrics exist!")
        for line in self.lyrics:
            words = line.split()
            model.update([(words[i], words[i+1]) for i in range(len(words)-1)]) # safe since range(-1) = []
        self.bigrams = model

    def create_trigram_model(self):
        model = Counter()
        if len(self.lyrics) == 0:
            raise Exception("No lyrics exist!")
        for line in self.lyrics:
            words = line.split()
            model.update([(words[i], words[i+1], words[i+2]) for i in range(len(words)-2)])
        self.trigrams = model


##########################################################
#
#   TEST CODE
# -------------
# If you're not concerned with testing the SongParser
# class, you can stop here. Nothing below is of interest.
#
##########################################################
def main():
    sp = SongParser()
    # Raw lyrics parsing is tentatively successful!
    # More extensive tests probably needed, these are like passing grader.py.
    if "parse" in sys.argv:
        sp.parse_song("Owl City || Dementia.txt")
        print "\n"
        for line in sp.lyrics:
            print line
        print sp.lyrics

        sp.parse_song("Eminem || Kill You.txt")
        print "\n"
        for line in sp.lyrics:
            print line
        print sp.lyrics

        sp.parse_song("Bastille || Laughter Lines.txt")
        print "\n"
        for line in sp.lyrics:
            print line
        print sp.lyrics

    # This is tentatively successful too!
    if "model" in sys.argv:
        sp.parse_song("Bastille || Laughter Lines.txt")
        sp.create_unigram_model()
        sp.create_bigram_model()
        sp.create_trigram_model()
        print sp.unigrams, '\n', sp.bigrams, '\n', sp.trigrams

    # As is this one!
    if "cons" in sys.argv:
        cp = SongParser("Owl City || Dementia.txt")
        print cp.lyrics
        print cp.unigrams, '\n', cp.bigrams, '\n', cp.trigrams


if __name__ == '__main__':
    main()
