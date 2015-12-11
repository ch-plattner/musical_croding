import math
import random
import collections
import Artist
import os

LINE_LENGTH_MIN = 8
LINE_LENGTH_MAX = 12
EPSILON = 0.20

UNIGRAM_WEIGHT  = 1
BIGRAM_WEIGHT   = 10
TRIGRAM_WEIGHT  = 100

# Preparatory code: Setting Up All Artists' N-grams
# -------------------------------------------------
# Uni/bi/tri-grams from ALL of our artists are stored in /Data/unigrams.txt,
# /Data/bigrams.txt, and /Data/trigrams.txt. We read these files and parse
# them for later use in generate_one_line().

REPO_ROOT = os.popen("git rev-parse --show-toplevel").read().strip('\n')

UNIVERSAL_UNIGRAMS = {}
UNIVERSAL_BIGRAMS = {}
UNIVERSAL_TRIGRAMS = {}

f = open(REPO_ROOT + '/Data/unigrams.txt', 'r')
line = f.readline()
# Go through file, read each line of < word ... word || freq > and register it in the dict.
while line != "":
    unigram = line.split('||')[0].strip()
    freq = int(line.split('||')[1].strip())
    UNIVERSAL_UNIGRAMS[unigram] = freq
    line = f.readline()

f = open(REPO_ROOT + '/Data/bigrams.txt', 'r')
line = f.readline()
# Go through file, read each line of < word ... word || freq > and register it in the dict.
while line != "":
    gram = line.split('||')[0].strip().split()
    bigram = (gram[0], gram[1])
    freq = int(line.split('||')[1].strip())
    UNIVERSAL_BIGRAMS[bigram] = freq
    line = f.readline()

f = open(REPO_ROOT + '/Data/trigrams.txt', 'r')
line = f.readline()
# Go through file, read each line of < word ... word || freq > and register it in the dict.
while line != "":
    gram = line.split('||')[0].strip().split()
    trigram = (gram[0], gram[1], gram[2])
    freq = int(line.split('||')[1].strip())
    UNIVERSAL_TRIGRAMS[trigram] = freq
    line = f.readline()



################################################


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
        trigram_score = (artist.trigrams[trigram] if (trigram in artist.trigrams) else 0) * \
                (artist.theme_values[trigram][theme] if (trigram in artist.theme_values) else 1)
        bigram = (second, word)
        bigram_score = (artist.bigrams[bigram] if (bigram in artist.bigrams) else 0) * \
                (artist.theme_values[bigram][theme] if (bigram in artist.theme_values) else 1)
        unigram = word
        unigram_score = (artist.unigrams[unigram] if (unigram in artist.unigrams) else 0) * \
                (artist.theme_values[unigram][theme] if (unigram in artist.theme_values) else 1)
        # If there is no trigram with (first, second, word) then DON'T include this word.
        # Continuing with a poor word will create a shitty lyric line.
        if trigram_score == 0:
            continue

        # This is the blender function to combine the three above.
        score = TRIGRAM_WEIGHT * math.log(trigram_score + 1.0) + BIGRAM_WEIGHT * math.log(bigram_score + 1.0) + UNIGRAM_WEIGHT * math.log(unigram_score + 1.0)
        weights[word] = score
    
    # NOTICE: This is going to have to chance once we implement external corpus epsilon, because a lot of sequences
    # of words will have no trigrams.
    # If we have NO words that will create a trigram next, then just end the line with !!END!!.
    if len(weights) == 0:
        return '!!END!!'
    return weightedRandomChoice(weights)

# Helper: Generate One Word (Epsilon version)
# -------------------------------------------
# Also generates one word, but from the UNIVERSAL grams data, not the artist-specific N-gram data.
#
def generate_one_word_epsilon(first, second):
    weights = {}

    for word in UNIVERSAL_UNIGRAMS:
        trigram = (first, second, word)
        trigram_score = UNIVERSAL_TRIGRAMS[trigram] if trigram in UNIVERSAL_TRIGRAMS else 0
        bigram = (second, word)
        bigram_score = UNIVERSAL_BIGRAMS[bigram] if bigram in UNIVERSAL_BIGRAMS else 0
        unigram = word
        unigram_score = UNIVERSAL_UNIGRAMS[unigram] # word must be in UNIVERSAL_UNIGRAMS.
        # If epsilon is activated, we need to be even safer: Do not pick next words not part of a trigram.
        if trigram_score == 0:
            continue

        score = TRIGRAM_WEIGHT * math.log(trigram_score + 1.0) + BIGRAM_WEIGHT * math.log(bigram_score + 1.0) + UNIGRAM_WEIGHT * math.log(unigram_score + 1.0)
        weights[word] = score * score # squared to bias toward higher-scored words, increase predictability to balance out extra randomness.

    # len(weights) should NEVER be 0, because the current artist's trigrams are inside UNIVERSAL_TRIGRAMS also, and these will also be valid trigrams to pick from.
    # ... but it's breaking anyway. fuck.
    return weightedRandomChoice(weights)

# Function: Generate One Line
# ---------------------------
# Generate one line of a song. Returned as a list of words.
#
def generate_one_line(artist, theme=1, epsilon=0.0):
    length_upper_bound = random.randint(LINE_LENGTH_MIN, LINE_LENGTH_MAX)
    first_trigram = get_first_trigram(artist, theme)
    
    line = [first_trigram[0], first_trigram[1], first_trigram[2]]
    
    first = first_trigram[1]
    second = first_trigram[2]

    for i in range(0, length_upper_bound - 3):
        # At a |epsilon| chance, we pick a word outside of our artist's corpus. We instead pick a word from the
        # combined corpus of all artists.
        if (random.random() < epsilon):
            next_word = generate_one_word_epsilon(first, second)
        else: 
            next_word = generate_one_word(artist, first, second, theme)
            # Stop prematurely if '!!END!!' is received, because of reasons detailed in generate_one_word.
            if next_word == '!!END!!':
                break
        line.append(next_word)
        first = line[len(line)-2]
        second = line[len(line)-1]
    return line


