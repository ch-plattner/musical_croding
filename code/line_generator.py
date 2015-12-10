import math
import random
import collections
import Artist

LINE_LENGTH_MIN = 8
LINE_LENGTH_MAX = 14

UNIGRAM_WEIGHT  = 1
BIGRAM_WEIGHT   = 5
TRIGRAM_WEIGHT  = 10


# Function: Weighted Random Choice
# --------------------------------
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

# Helper: Get First Trigram
# ---------------------------
# Pick a random trigram under the Artist.
#
def get_first_trigram(artist, theme):
    weights = artist.trigrams
    for trigram in weights:
        weights[trigram] = weights[trigram]*TRIGRAM_WEIGHT*artist.theme_values[trigram][theme] \
            + artist.bigrams[(trigram[0], trigram[1])]*BIGRAM_WEIGHT*artist.theme_values[(trigram[0], trigram[1])][theme] \
            + artist.unigrams[trigram[0]]*artist.theme_values[trigram[0]][theme]
        weights[trigram] = math.log(weights[trigram] + 1.0)
    return weightedRandomChoice(weights)

# Helper: Generate One Word
# -------------------------
# Given the last 2 words, generate a next word based on the artist and the theme.
#
def generate_one_word(artist, first, second, theme):
    weights = {}

    for word in artist.unigrams:
        # Create independent uni, bi, tri-gram scores.
        trigram = (first, second, word)
        trigram_score = TRIGRAM_WEIGHT * (artist.trigrams[trigram] if (trigram in artist.trigrams) else 0) * \
                (artist.theme_values[trigram][theme] if (trigram in artist.theme_values) else 0)
        bigram = (second, word)
        bigram_score = BIGRAM_WEIGHT * (artist.bigrams[bigram] if (bigram in artist.bigram) else 0) * \
                (artist.theme_values[bigram][theme] if (bigram in artist.theme_values) else 0)
        unigram = word
        unigram_score = UNIGRAM_WEIGHT * (artist.unigrams[unigram] if (unigram in artist.unigrams) else 0) * \
                (artist.theme_values[unigram][theme] if (unigram in artist.theme_values) else 0)

        # This is the blender function to combine the three above.
        score = trigram_score + bigram_score + unigram_score
        weights[word] = math.log(score + 1.0)

        return weightedRandomChoice(weights)


"""


    for trigram in artist.trigrams:
        if trigram[0] == first and trigram[1] == second:
            weights[trigram] = artist.trigrams[trigram]*TRIGRAM_WEIGHT*artist.theme_values[trigram][theme]  \
                + artist.bigrams[(first, second)]*BIGRAM_WEIGHT*artist.theme_values[(first, second)][theme]  \
                + artist.unigrams[trigram[2]]*artist.theme_values[trigram[2]][theme]
            weights[trigram] = math.log(weights[trigram] + 1.0)
    if len(weights) == 0:
        return "!!END!!"
    else: 
        return weightedRandomChoice(weights)[2]
"""
        
# Function: Generate One Line
# ---------------------------
# Generate one line of a song.
#
def generate_one_line(artist, theme=1, epsilon=0.0):
    length_upper_bound = random.randint(LINE_LENGTH_MIN, LINE_LENGTH_MAX)
    first_trigram = get_first_trigram(artist, theme)
    line = " ".join(first_trigram) + " "
    first = first_trigram[1]
    second = first_trigram[2]
    for i in range(0, length_upper_bound - 3):
        if (random.random() < epsilon):
### NEW
            next_word = weightedRandomChoice(artist.unigrams)
### /NEW
        else: 
            next_word = generate_one_word(artist, first, second, theme)
        
        line += next_word + " "
        first = second
        second = next_word
    return line

# Function: Generate Stanza (one level above Line)
# ------------------------------------------------
# self explanatory. Generate 1 verse/chorus/bridge.
#
def generate_stanza(artist, length, theme=1):
    stanza = ""
    for i in range(0, length):
        stanza += generate_one_line(artist, theme, 0.15) + '\n'
    return stanza

# Function: Generate Song Lyrics (one level above Stanza)
# -------------------------------------------------------
# Generates an entire song. The structure was hardcoded.
#
def generate_song_lyrics(artist, theme=1):
    verse_length = random.randint(8, 14)
    chorus_length = random.randint(verse_length - 2, verse_length + 2)
    verse1 = "[Verse 1]\n" + generate_stanza(artist, verse_length, theme) +  "\n"
    verse2 = "[Verse 2]\n" + generate_stanza(artist, verse_length, theme) +  "\n"
    chorus = "[Chorus]\n"  + generate_stanza(artist, chorus_length, theme) +  "\n"
    bridge = "[Bridge]\n"  + generate_stanza(artist, verse_length / 2, theme) +  "\n"
    return "".join([verse1, chorus, verse2, bridge, chorus, chorus])

