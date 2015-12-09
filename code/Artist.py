import os, sys
from os import path
from collections import Counter
import SongParser
import song_cluster

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
#   theme_values| = {word1 : {0: 5, 1: 10, 2: 15}, word2 : ... } => links words to their counts in each cluster
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
        self.update_clusters()
        self.update_models()

    # Function: register_all_songs
    # ----------------------------
    # Given the artist, browses through all of the songs under that artist
    # and creates a SongParser for each.
    def register_all_songs(self, artist):
        files = os.listdir(os.path.join(self.root, artist))
        self.songs = [SongParser.SongParser(entry) for entry in files if os.path.isfile(os.path.join(self.root, artist, entry)) and entry != '.DS_Store']
       
    # Function: update_clusters
    # ----------------------------
    # Clusters all the songs by the artist into 3 themes.
    def update_clusters(self):
        print "About to start theme clustering..."
        print "Please be patient."
        self.clusters = song_cluster.find_theme_clusters_by_artist(self.name)
        print self.clusters

    # Function: get_cluster_number
    # ----------------------------
    # Given a song, returns the cluster number of the theme it belongs to.
    def get_cluster_number(self, song):
        for cluster_number in self.clusters:
            if song in self.clusters[cluster_number]:
                return cluster_number
        print "Warning: incorrect clustering"
        return -1

    # Function: normalize
    # ----------------------------
    # Given a dictionary, returns the dictionary with its values normalized.
    def normalize(self, d, target=1.0):
       raw = sum(d.values())
       factor = target/raw
       return {key:value*factor for key,value in d.iteritems()}


    # Function: update_theme_values
    # ----------------------------
    # Given unigram, bigram and trigram counts for one song, this updates the
    # self.theme_values dictionary.
    def update_theme_values(self, unigrams, bigrams, trigrams, cluster_number):
        for value in unigrams:
            if value not in self.theme_values:
                self.theme_values[value] = {0:100, 1:100, 2:100}
            self.theme_values[value][cluster_number] += unigrams[value]
        for value in bigrams:
            if value not in self.theme_values:
                self.theme_values[value] = {0:100, 1:100, 2:100}
            self.theme_values[value][cluster_number] += bigrams[value]
        for value in trigrams:
            if value not in self.theme_values:
                self.theme_values[value] = {0:100, 1:100, 2:100}
            self.theme_values[value][cluster_number] += trigrams[value]
        for ngram in self.theme_values:
            self.theme_values[ngram] = self.normalize(self.theme_values[ngram])

    # Function: update_models
    # -----------------------
    # Creates unigram, bigram, and trigram models for the artist by aggregating
    # the respective weights from all of their songs.
    # Note: We need laplace smoothing. What |lambda| value is, we can learn.
    def update_models(self):
        uni = Counter()
        bi = Counter()
        tri = Counter()
        self.theme_values = {}
        for song in self.songs:
            song_unigrams = song.unigrams
            song_bigrams = song.bigrams
            song_trigrams = song.trigrams

            cluster_number = self.get_cluster_number(song.name.split(' || ')[1].replace('.txt', '').strip())
            self.update_theme_values(song_unigrams, song_bigrams, song_trigrams, cluster_number)
            
            uni.update(song_unigrams)
            bi.update(song_bigrams)
            tri.update(song_trigrams)
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
# def main():
#     artist = Artist("Taylor Swift")
#     # print artist.songs
#     # for song in artist.songs:
#         # print song.name, song.word_count, song.min_line, song.max_line, song.mean_line
#     # print artist.unigrams
#     # print artist.bigrams
#     # print artist.trigrams


# if __name__ == '__main__':
#     main()
