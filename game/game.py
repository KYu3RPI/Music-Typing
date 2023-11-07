import pygame
from song import Song

# Game class that controls the vars in the game
class Game:
    def __init__(self, song):
        self.__song = song
        self.__score = 0
        self.__currentStanza = 0 # index of the current stanza
        self.__currentLetter = 0 # index of the current letter that the player needs to type
        self.__previousLine = 0 # index of the previous line
        self.__currentLine = 1 # index of the next line
        self.__nextLine = 2 # index of the next line
        self.__mistakes = "" # string of the mistakes made by the player
        self.__currentwpm = 0
        self.__avgwpm = 0
        self.__accuracy = 0 # number of correct letters
        self.__totalLetters = 0 # total number of letters typed

    def getSong(self):
        return self.__song
    
    def getSongAudio(self):
        audio = self.getSong().getAudioFile()
        if audio.endswith(".mp3"):
            return audio
        else:
            # it is a youtube link so download the audio
            # for now does nothhing
            return
        return
    
    def getScore(self):
        return self.__score
    
    def getCurrentWPM(self):
        return self.__currentwpm
    
    def getAvgWPM(self):
        return self.__avgwpm
    
    def getAccuracy(self):
        if self.__totalLetters == 0:
            return 0
        return self.__accuracy/self.__totalLetters
    
    def getTotalLetters(self):
        return self.__totalLetters
    
    def updateScore(self):
        self.__score += 2 + 3 * self.getAccuracy() + 0.5 * self.getCurrentWPM()
    
    def getPreviousLyric(self):
        # if index is -1 then return empty string
        if self.__previousLine == 0:
            return ""
        # else return the previous lyric
        return self.getSong().getLyrics()[self.__currentStanza][self.__previousLine]
    
    def getCurrentLyric(self):
        return self.getSong().getLyrics()[self.__currentStanza][self.__currentLine]
    
    def getNextLyric(self):
        # if out of bounds then return empty string
        if self.__nextLine >= len(self.__song.getLyrics()[self.__currentStanza]):
            return ""
        return self.getSong().getLyrics()[self.__currentStanza][self.__nextLine]
    
    # returns the portion of the lyrics that's been typed as a string
    def getTypedLyric(self):
        return self.getSong().getLyrics()[self.__currentStanza][self.__currentLine][:self.__currentLetter]
    
    def getMistakes(self):
        return self.__mistakes
    
    # typing related functions

    # function to call when current line is done being typed
    # returns -1 if the song is over
    # and a 1 if there is more to type
    def nextLyric(self):
        # update lines and letter
        self.__currentLetter = 0
        self.__previousLine += 1
        self.__currentLine += 1
        self.__nextLine += 1
        # check if the stanza is done
        if len(self.getSong().getLyrics()[self.__currentStanza]) == self.__currentLine:
            # if it is then update the stanza
            self.__currentStanza += 1
            self.__previousLine = 0
            self.__currentLine = 1
            self.__nextLine = 2
        # check if the song is over
        if len(self.getSong().getLyrics()) - 1 == self.__currentStanza:
            # if it is then return to main
            return -1
        return 1

    # function to call when the player types a letter
    # typedLetter is the unicode of the typed letter
    # returns 0 when the line is not done being typed
    # returns 1 when the line is done being typed
    # returns -1 when the song is over
    def typeLetter(self, typedLetter):
        self.__totalLetters += 1
        # check if the letter is correct
        #if typedLetter.isalpha():
        #    print(self.getCurrentLyric()[:(self.__currentLetter + 1)], "|", (self.getTypedLyric() + self.__mistakes + typedLetter))
        if self.getCurrentLyric()[:(self.__currentLetter + 1)] == (self.getTypedLyric() + self.__mistakes + typedLetter):
            # if it is correct then update accuracy
            self.__accuracy += 1
            self.__currentLetter += 1
            self.updateScore()
            # then check if the line is done being typed
            if self.__currentLetter == len(self.getSong().getLyrics()[self.__currentStanza][self.__currentLine]):
                return self.nextLyric()
        else:
            # the letter is inaccurate so add it to the mistakes
            self.__mistakes += typedLetter
        return 0

    # user deletes a mistake letter that they typed
    # is only called when they are getting rid of a mistake
    def backspace(self):
        # remove the last letter from the mistakes
        self.__mistakes = self.__mistakes[:-1]

    # time related functions

    # function that returns when the current stanza starts
    def getCurrentStanzaStart(self):
        return self.getSong().getLyrics()[self.__currentStanza][0]

    # function that returns when the next stanza starts/ current stanza ends
    def getNextStanzaStart(self):
        # check if the song is over
        if self.__currentStanza == len(self.getSong().getLyrics()):
            # if it is then return -1
            return -1
        # else return the start of the next stanza
        return self.getSong().getLyrics()[self.__currentStanza + 1][0]
    
    def nextStanza(self):
        self.__currentStanza += 1
        self.__previousLine = 0
        self.__currentLine = 1
        self.__nextLine = 2
        self.__currentLetter = 0
        self.__mistakes = ""
        if self.__currentStanza == len(self.getSong().getLyrics()) - 1:
            return -1
        return 1