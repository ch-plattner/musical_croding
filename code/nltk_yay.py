import nltk
import song_parsing

class NLTKParser:
	def __init__(self):
		self.artists = song_parsing.get_list_of_artists()

	def testing(self):
		songs = song_parsing.get_all_song_lyrics(self.artists[0])
		for song in songs:
			print songs[song]
			lyrics = nltk.word_tokenize(songs[song])
			# print set(nltk.pos_tag(lyrics))

			bigrams = list(nltk.bigrams(lyrics)) # Get list of bigrams
			print bigrams

			trigrams = list(nltk.trigrams(lyrics))
			# print trigrams

			fdist = nltk.FreqDist(bigrams) # Create frequency distribution
			# print fdist.most_common(5) # Print 5 most common samples
			
			break

def main():
	nltk = NLTKParser()
	nltk.testing()

if __name__ == "__main__":
    main()
