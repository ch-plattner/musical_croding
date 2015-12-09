import os, sys
from os import path
from collections import Counter
import SongParser

# Class: Artist
# -----------------
# The object for interacting with an individual artist.
# 
# Attributes: |self.
#   root| = the lyrics directory relative to the Git repo, for convenience.
#   name| = the name of the artist.
#   songs| = a list of all the artist's songs' SongParsers.
#   unigram|,
#   bigram|,
#   trigram| = dicts from (uni/bi/trigram) : weight
#

#########      UNTESTED          ##################

class Artist:
    # Constructor: Artist
    # -----------------------
    # |artist| is the name of the artist as it appears in /Data/lyrics.
    def __init__(self, artist):
        self.root = os.popen("git rev-parse --show-toplevel").read().strip('\n') + "/Data/lyrics/"
        self.name = artist
        self.register_all_songs(artist)
        self.update_models()


    # Function: register_all_songs
    # ----------------------------
    # Given the artist, browses through all of the songs under that artist
    # and creates a SongParser for each.
    def register_all_songs(self, artist):
        files = os.listdir(os.path.join(self.root, artist))
        self.songs = [SongParser.SongParser(entry) for entry in files if os.path.isfile(os.path.join(self.root, artist, entry)) and entry != '.DS_Store']
            
    # Function: update_models
    # -----------------------
    # Creates unigram, bigram, and trigram models for the artist by aggregating
    # the respective weights from all of their songs.
    # Note: We need laplace smoothing. What |lambda| value is, we can learn.
    def update_models(self):
        uni = Counter()
        bi = Counter()
        tri = Counter()
        for song in self.songs:
            uni.update(song.unigrams)
            bi.update(song.bigrams)
            tri.update(song.trigrams)
        self.unigrams = uni
        self.bigrams = bi
        self.trigrams = tri

##########################################################
#
#   TEST CODE
# -------------
# If you're not concerned with testing the Artist
# class, you can stop here. Nothing below is of interest.
#
##########################################################
def main():
    artist = Artist("Taylor Swift")
    print artist.songs
    for song in artist.songs:
        print song.name, song.word_count, song.min_line, song.max_line, song.mean_line
    # print artist.unigrams
    # print artist.bigrams
    # print artist.trigrams


if __name__ == '__main__':
    main()
