import os

REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')

# Class: SongParser
# -----------------
# ???
#
class SongParser:
    def __init__(self):
        pass

    def parse_song(self, raw_lyrics):
        pass

# Function: get_list_of_artists
# -----------------------------
# 
def get_list_of_artists():
    artists = []
    artists_file = open(REPO_ROOT + '/Data/lyrics/artists.txt', 'r')
    for artist in artists_file:
        artists.append(artist.strip())
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
        song_name = song_filename.split(' || ')[1].replace('.txt', '').strip()
        lyrics = open(artist_root_dir + song_filename.strip()).read()
        songs[song_name] = lyrics
    
    return songs


