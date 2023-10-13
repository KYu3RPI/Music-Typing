import pygame
from song import Song

# Game class
class Game:
    def __init__(self, song):
        self.__song = song
        self.__score = 0
        # set background to light blue for now
        self.__background = (173,216,230)
        # check if audio file is a .ogg file or a youtube link
        if (self.__song.getAudioFile().endswith(".ogg")):
            # load the audio file
            pygame.mixer.music.load(self.__song.getAudioFile())
        else:
            # load the audio from the youtube link
            pass

    def start(self):
        # initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((1280,720))
        pygame.display.set_caption("Music Typing")
        clock = pygame.time.Clock()
        # light blue color
        screen.fill(self.__background)

        while True:
            # update the display
            pygame.display.update()

            # Process player inputs.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            # update the display
            pygame.display.update()
            pass

    def update(self):
        pass