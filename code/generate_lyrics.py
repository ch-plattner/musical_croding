import song_parsing 

def main():
    print "Welcome to Lyrics Generator! Let's make a song."
    print "Setting up artist database..."
    artist_database = song_parsing.get_list_of_artists()

    # Get artist
    while True:
        artist = raw_input("What artist would you like to emulate? (Press enter to exit.) ").strip()
        if artist == "": 
            break
        if artist not in artist_database:
            print "That artist is not in our database!\n"
        else:
            print "Let's make a", artist, "song..."
            print "Give us a few seconds to train our database...\n"
            songs = song_parsing.get_all_song_lyrics(artist)
            lyrics = generate_song_lyrics(artist)

# Given a song and a model, generates a valid song
def generate_song_lyrics(artist):
    pass

main()