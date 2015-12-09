import random

LINE_LENGTH_MIN = 8
LINE_LENGTH_MAX = 14

def generate_one_word(artist, first, second):
    # First, we create a weighted dictionary that holds all the unigrams
    # linked to their frequencies
    weights = artist.unigrams

    for word in weights:
        # Update the word weight with its bigram frequencies
        if (second != None):
            pass

        # Update the word weight with its trigram frequencies
        if (first != None): 
            pass

        # Update the word weight with its theme score

    return weightedRandomChoice(weights)


def generate_one_line(artist, theme=None, epsilon=0.0):
    length = random.randint(LINE_LENGTH_MIN, LINE_LENGTH_MAX)
    first, second, line = None, None, ""
    for i in range(0, length):
        if (random.random() < epsilon):
            next_word = "RAND"
        else: 
            next_word = generate_one_word(artist, first, second)
        
        line += next_word + " "
        first = second
        second = next_word
    return line

print generate_one_line(None, None, 0.5)

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