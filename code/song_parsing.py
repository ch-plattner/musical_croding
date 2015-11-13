class SongParser:
    def __init__(self):
        pass

    def parse_song(self, raw_lyrics):
        pass

# Returns a list of all artists in our database
def get_list_of_artists():
    artists = []
    artists_file = open('../lyrics/artists.txt', 'r')
    for artist in artists_file:
        artists.append(artist.strip())
    return artists

# Create model for the specified artist
def get_all_song_lyrics(artist):
    songs = {}
    root_dir = '../lyrics/' + artist + '/'
    list_of_songs = open(root_dir + 'songs.txt', 'r')
    for song_filename in list_of_songs:
        song_name = song_filename.split(' - ')[2].replace('.txt', '').strip()
        lyrics = open(root_dir + song_filename.strip()).read()
        songs[song_name] = lyrics
    return songs


