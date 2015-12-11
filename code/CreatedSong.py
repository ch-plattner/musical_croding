import random
import line_generator
import copy

MU = 0.20

class CreatedSong:
    def __init__(self, artist, theme=1):
        self.song_lyrics = self.generate_song_lyrics(artist, theme) 


    # Function: Generate Stanza (one level above generate_one_line() in line_generator.py)
    # ------------------------------------------------------------------------------------
    # self explanatory. Generate 1 verse/chorus/bridge.
    #
    def generate_stanza(self, artist, length, theme):
        stanza = []
        
        for i in range(0, length):
            # With chance MU on an even-numbered line that is not line 2, repeat the last line.
            if (i % 2) == 1 and i != 1 and not last_line_was_a_copy and random.random() < MU:
                stanza.append(copy.deepcopy(stanza[i-1]))
                last_line_was_a_copy = True
            # Generate another line and add it to the stanza.
            else:
                stanza.append(line_generator.generate_one_line(artist, theme, line_generator.EPSILON))
                if i % 2 == 1:
                    last_line_was_a_copy = False
        return stanza

    # Function: Generate Song Lyrics (one level above Stanza)
    # -------------------------------------------------------
    # Generates an entire song. The structure was hardcoded.
    #
    def generate_song_lyrics(self, artist, theme=1):
        verse_length = random.randint(8, 14)
        chorus_length = random.randint(verse_length - 2, verse_length + 2)
        verse1 = self.generate_stanza(artist, verse_length, theme)
        verse2 = self.generate_stanza(artist, verse_length, theme)
        chorus = self.generate_stanza(artist, chorus_length, theme)
        bridge = self.generate_stanza(artist, verse_length / 2, theme)
        return {"V1":verse1, "V2":verse2, 'BR':bridge, 'CH':chorus}

####################################
    # Helper: Print Block
    # -------------------
    # Prints one block of lyrics. A block is a list of lines,
    # where each line is a list of words.
    def print_block(self, block):
        for line in block:
            print ' '.join(line)
        print '\n'

    # Function: Print This Song
    # -------------------------
    # Prints the song properly, from the information inside |self.song_lyrics|.
    # Unpacks all the nested lists and formats correctly.
    # Note that:
    # |self.song_lyrics| should be a dict of 4 blocks, each block is a list of some lines.
    def print_this_song(self):
        lyrics = self.song_lyrics
        print '\n'

        print "[Verse 1]"
        self.print_block(lyrics["V1"])

        print "[Chorus]"
        self.print_block(lyrics["CH"])

        print "[Verse 2]"
        self.print_block(lyrics["V2"])

        print "[Chorus]"
        self.print_block(lyrics["CH"])

        print "[Bridge]"
        self.print_block(lyrics["BR"])

        print "[Chorus]"
        self.print_block(lyrics["CH"])




