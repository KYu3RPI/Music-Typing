# create song class

class Song:
    def __init__(self, inputfile):
        self.__inputfile = inputfile
        self.__title = ""
        self.__artist = ""
        self.__bpm = 0
        self.__audio_file = ""
        self.__background_file = ""
        self.__lyrics = [] # list of lists, the first value of each list being the time in sec and the rest of the values being the lyrics of the stanza

    def parseSong(self):
        # get a list of lines from the input file and remove empty lines and comment lines
        print(self.__inputfile)
        with open(self.__inputfile, 'r') as file:
            lines = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]
        
        # get the song info
        self.__title = lines[0]
        self.__audio_file = lines[1]

        # get the lyrics
        stanza = []
        for i in range(2, len(lines)):
            # if stanza is empty then you get the time of the stanza
            if not stanza and lines[i].split(":")[0].isnumeric():
                # get the time of the stanza
                time = lines[i].split(":")
                # convert the time into seconds
                time = int(time[0]) * 60 + int(time[1])
                # append the time to the stanza
                stanza.append(time)
            # if the stanza is not empty then check if it lyric or time
            else:
                # if it is a time then append stanza to lyrics and clear stanza
                if int(lines[i].split(":")[0].isnumeric()):
                    self.__lyrics.append(stanza)
                    stanza = []
                    # get the time of the stanza
                    time = lines[i].split(":")
                    # convert the time into seconds
                    time = int(time[0]) * 60 + int(time[1])
                    # append the time to the stanza
                    stanza.append(time)
                # if it is a lyric then append lyric to stanza
                else:
                    stanza.append(lines[i])
        # append the last stanza to lyrics
        self.__lyrics.append(stanza)

        # function to print song object
    def printSong(self):
        print("Input File: " + self.__inputfile)
        print("Title: " + self.__title)
        print("Audio File: " + self.__audio_file)
        print("Lyrics: ")
        for stanza in self.__lyrics:
            print(stanza)
        print("")