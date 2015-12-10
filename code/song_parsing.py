import os
import SongParser
from collections import Counter
import Artist
import types

REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')

# Function: get_list_of_artists
# -----------------------------
# 
def get_list_of_artists():
    artists = []
    artists_file = open(REPO_ROOT + '/Data/lyrics/artists.txt', 'r')
    for artist in artists_file:
        artists.append(artist.strip())
    artists_file.close()
    return artists

# Function: get_all_song_lyrics
# -----------------------------
# Input: The name of the artist whose song lyrics we would like, as a stringi.
#
# Output: A dictionary representing the lyrics of each song from ONE artist.
#         Key: The title of a song from the artist.
#         Value: The entire raw text of the song, line breaks and all, as a string.
#           (WARNING: the lyrics might have noisy symbols and comments. Hence raw.)
def get_all_song_lyrics(artist):
    songs = {}
    artist_root_dir = REPO_ROOT + '/Data/lyrics/' + artist + '/'

    for song_filename in os.listdir(artist_root_dir):
        if song_filename == '.DS_Store':
            continue

        song_name = song_filename.split(' || ')[1].replace('.txt', '').strip()
        lyrics = open(artist_root_dir + song_filename.strip()).read()
        songs[song_name] = lyrics
    
    return songs

# Function: get_all_ngrams
# -----------------------------
# Output: Counts unigrams, bigrams, and trigrams from all lyrics files and
# outputs them to unigrams.txt, bigrams.txt, and trigrams.txt
def get_all_ngrams():
    unigrams = Counter()
    bigrams = Counter()
    trigrams = Counter()
    artists = get_list_of_artists()
    for artist_name in artists:
        artist = Artist.Artist(artist_name)
        unigrams += artist.unigrams
        bigrams += artist.bigrams
        trigrams += artist.trigrams
    write_to_file(unigrams, REPO_ROOT + '/Data/unigrams.txt')
    write_to_file(bigrams, REPO_ROOT + '/Data/bigrams.txt')
    write_to_file(trigrams, REPO_ROOT + '/Data/trigrams.txt')

# Function: write_to_file
# -----------------------------
# Input: A counter object containing either strings or tuples mapped to their counts,
#        and a path to a file to be written to
# Output: Writes the ngram counts to the given file path
def write_to_file(counter, file_path):
    ngram_file = open(file_path, 'w')
    for word in counter:
        if type(word) is types.StringType:
            string = word
        else:
            string = ' '.join([w for w in word])
        ngram_file.write(string + ' || ' + str(counter[word]) + '\n')
    ngram_file.close()
