import song_parsing 
import string
import collections
import random
import Artist
import line_generator

def main():
    print "Welcome to Lyrics Generator! Let's make a song."
    print "Setting up artist database..."
    artist_database = song_parsing.get_list_of_artists()

    # Get artist_name
    while True:
        artist_name = raw_input("What artist would you like to emulate? (Press enter to exit.) ").strip()
        if artist_name == "": 
            break
        if artist_name not in artist_database:
            print "That artist is not in our database!\n"
        else:
            print "Let's make a", artist_name, "song..."
            print "Give us a few seconds to train our database...\n"
            #lyrics = generate_song_lyrics_baseline(artist_name, 300)
            artist = Artist.Artist(artist_name)
            print line_generator.generate_song_lyrics(artist)

###################################################################

# Function: Weighted Random Choice
# --------------------------------
# TAKEN FROM CS221 ASSIGNMENT CAR, |util.py|
# Given a dictionary of the form element -> weight, selects an element
# randomly based on distribution proportional to the weights. Weights can sum
# up to be more than 1. 
def weightedRandomChoice(weightDict):
    weights = []
    elems = []
    for elem in weightDict:
        weights.append(weightDict[elem])
        elems.append(elem)
    total = sum(weights)
    key = random.uniform(0, total)
    runningTotal = 0.0
    chosenIndex = None
    for i in range(len(weights)):
        weight = weights[i]
        runningTotal += weight
        if runningTotal > key:
            chosenIndex = i
            return elems[chosenIndex]
    raise Exception('Should not reach here')

# Function: Generate Song Lyrics, Baseline
# ----------------------------------------
# Given an artist, generates a valid song. Very crude.
# This function returns a random sequence of |num_words| 
# words used in this artist's songs, with the probability of
# a given word being selected being proportional to its frequency
# in the artist's corpus of lyrics.
def generate_song_lyrics_baseline(artist, num_words):

    # This is a dictionary of (key=|song name| : value=|entire raw text|)
    # for every |song name| sung by the given |artist|.
    songs = song_parsing.get_all_song_lyrics(artist)
    
    # Input: the raw text of one song's lyrics as a string.
    # Output: a Counter() with the frequencies of each word in the song's lyrics.
    def createLyricsVocabularyCounter(lyrics):
        raw_words = lyrics.split()
        processed_words = [word.strip(".,:[]{}()") for word in raw_words]
        return collections.Counter(processed_words)

    listOfCounters = [createLyricsVocabularyCounter(songs[title]) for title in songs]

    def combine_two_counters(c1, c2):
        out = collections.Counter()
        out.update(c1)
        out.update(c2)
        return out

    total_artist_word_frequencies = reduce(combine_two_counters, listOfCounters)
    generated_words = [weightedRandomChoice(total_artist_word_frequencies) for _ in range(num_words)]
    return ' '.join(generated_words)
    

main()
