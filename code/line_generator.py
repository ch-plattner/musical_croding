import math
import random
import collections
import Artist

LINE_LENGTH_MIN = 8
LINE_LENGTH_MAX = 14

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

def generate_one_word(artist, first, second):
    # TO DO: Update the word weight with its theme weights

    # First word in the line
    if (second == None):
        weights = artist.trigrams
        for trigram in weights:
            weights[trigram] = math.log(weights[trigram]*10 + artist.bigrams[(trigram[0], trigram[1])]*5
                + artist.unigrams[trigram[0]])
       
        return weightedRandomChoice(weights)[0]

    # Second word in the line
    if (first == None):
        weights = {}
        for trigram in artist.trigrams:
            if trigram[0] == second:
                weights[trigram] = math.log(artist.trigrams[trigram]*10 + artist.bigrams[(second, trigram[1])]*5
                    + artist.unigrams[second])
        return weightedRandomChoice(weights)[1]

    # All other words
    weights = {}
    for trigram in artist.trigrams:
        if trigram[0] == first and trigram[1] == second:
            weights[trigram] = math.log(artist.trigrams[trigram]*10 + artist.bigrams[(first, second)]*5
                + artist.unigrams[trigram[2]])
    if len(weights) == 0:
        return "!!END!!"
    else: 
        return weightedRandomChoice(weights)[2]
        
        
def generate_one_line(artist, theme=None, epsilon=0.0):
    length_upper_bound = random.randint(LINE_LENGTH_MIN, LINE_LENGTH_MAX)
    first, second, line = None, None, ""
    for i in range(0, length_upper_bound):
        if (random.random() < epsilon):
            next_word = "RAND"
        else: 
            next_word = generate_one_word(artist, first, second)
            if next_word == "!!END!!":
                break;
        
        line += next_word + " "
        first = second
        second = next_word
    return line

def generate_stanza(artist, length):
    stanza = ""
    for i in range(0, length):
        stanza += generate_one_line(artist) + '\n'
    return stanza

def generate_song_lyrics(artist):
    verse_length = random.randint(8, 14)
    chorus_length = random.randint(verse_length - 2, verse_length + 2)
    verse1 = "[Verse 1]\n" + generate_stanza(artist, verse_length) +  "\n"
    verse2 = "[Verse 2]\n" + generate_stanza(artist, verse_length) +  "\n"
    chorus = "[Chorus]\n"  + generate_stanza(artist, chorus_length) +  "\n"
    bridge = "[Bridge]\n"  + generate_stanza(artist, verse_length / 2) +  "\n"
    return "".join([verse1, chorus, verse2, bridge, chorus, chorus])

