from collections import Counter
import numpy as np

import sklearn.cluster
import sklearn.decomposition

import nltk
from nltk.stem.snowball import SnowballStemmer
import song_parsing

# This list contains the nltk part of speech codes for the parts of speech we want to cluster with.
# This includes nouns, adjectives, verbs, and adverbs.
DESIRED_POS = ['IN', 'JJ', 'JJR', 'JJS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'RB', 'RBR', 'RBS', 'VB', 
    'VBD', 'VBG', 'VBN', 'VBZ']

# function: get_all_words_and_word_counts
# ---------------------------------------
# @param songs : dictionary of song titles to lyrics of the song
# @return - list of all the words in all of the song lyrics in songs, in sorted order
#         - dictionary  of song titles to counter of all the nouns, adj, verbs, adverbs
#            in that song's lyrics, stemmed
def get_all_words_and_word_counts(songs):
    stemmer = SnowballStemmer("english")
    all_words = set([])
    song_counters = {}
    for song in songs:
        words = []
        for line in songs[song].split('\n'):
            t = nltk.word_tokenize(line.decode('utf-8'))
            
            words.extend(t) # remove this
            # tagged = nltk.pos_tag(t)
            # for word in tagged:
            #     if word[1] in DESIRED_POS:
            #        words.append(word[0])
                                
        # stemmed = []
        # for word in words: 
        #     try:
        #         stem = stemmer.stem(word)
        #     except:
        #         stem = word
        #     stemmed.append(stem)
        
        counter = Counter(words) # remove this                     
        #counter = Counter(stemmed)
        song_counters[song] = counter
        all_words = all_words.union( counter.iterkeys() )

    all_words = sorted(all_words)
    return all_words, song_counters
    
# function: get_all_representations_as_matrix
# ---------------------------------------
# @param songs : dictionary of song titles to lyrics of the song
# @param dictionary  of song titles to counter of all the nouns, adj, verbs, adverbs
#            in that song's lyrics, stemmed
# @param all_words : list of all the words in all of the song lyrics in songs, in sorted order
# @return a dictionary of cluster name to song titles in that cluster
def get_all_representations_as_matrix(songs, song_counters, all_words):
    all_song_representations = [[] for i in range(len(songs))]
    for word in all_words:
        for song_index, song in enumerate(songs):
            all_song_representations[song_index].append(song_counters[song[0]][word] * 1.0) 
    return all_song_representations
   
# function: get_clusters
# ---------------------------------------
# @param songs : dictionary of song titles to lyrics of the song
# @return a dictionary of cluster name to song titles in that cluster
def get_clusters(songs):
    N_CLUSTERS = 3

    all_words, song_counters = get_all_words_and_word_counts(songs)
    songs = list(songs.iteritems())
    
    all_song_representations = get_all_representations_as_matrix(songs, song_counters, all_words)
        
    #TF-IDF
    tfidf = sklearn.feature_extraction.text.TfidfTransformer(norm='l2',smooth_idf=True)
    communities = tfidf.fit_transform(all_song_representations).toarray()

    #SVD
    svd = sklearn.decomposition.TruncatedSVD(n_components=len(all_song_representations[0])/2)
    all_song_representations = svd.fit_transform(communities)
        
    clusterer = sklearn.cluster.KMeans(n_clusters=N_CLUSTERS, max_iter=500) #make max_iter higher later
    all_song_representations = np.array(all_song_representations) # as NP array
    cluster_labels = clusterer.fit_predict(all_song_representations)
    
    clusters = {}
    for song_index, cluster in enumerate(cluster_labels):
        if cluster not in clusters:
            clusters[cluster] = [songs[song_index][0]]
        else:
            clusters[cluster].append(songs[song_index][0])
    return clusters

# function: find_theme_clusters_by_artist
# ---------------------------------------
# @param artist : the artist whose songs we are clustering
# @return a dictionary of cluster name to song titles in that cluster 
def find_theme_clusters_by_artist(artist):
    songs = song_parsing.get_all_song_lyrics(artist)
    return get_clusters(songs)
