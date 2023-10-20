import pygame
from song import Song

# Game class that controls the vars in the game
class Game:
    def __init__(self, song):
        self.__song = song
        self.__score = 0
        self.__currentLine = 0

    def startGame(self):
        # start the display of the game
        # initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((1280,720))
        pygame.display.set_caption("Music Typing")
        clock = pygame.time.Clock()
        # light blue color
        screen.fill(self.getSong().getBackgroundFile())
        # button to go back to main
        backbutton = pygame.draw.rect(screen, (0,100,255), (100,100,100,50))
        # font
        font = pygame.font.Font('freesansbold.ttf', 32)
        # text
        backtext = font.render('Back', True, (160,160,160))
        # add text to button
        screen.blit(backtext, (110,110))

        while True:
            # update the display
            pygame.display.update()

            # Process player inputs.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("2")
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if the button is clicked
                    if backbutton.collidepoint(event.pos):
                        # go back to main
                        print("Back to Main")
                        return

            # update the display
            pygame.display.update()
            pass

    def updateScore(self):
        pass

    def endGame(self):
        pygame.mixer.music.unload()

    def getSong(self):
        return self.__song
    
    def getScore(self):
        return self.__score
    
    def getCurrentLyric(self):
        return self.__currentLine
    
    def nextLyric(self):
        self.__currentLine += 1