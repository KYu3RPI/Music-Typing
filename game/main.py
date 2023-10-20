from song import Song
from game import Game
import pygame
import pygame_menu
import os

def refresh(songDir):
    # clear songs list
    temp = []
    for song in os.listdir(songDir):
        # create song object
        songObj = Song(songDir + "\\" + song)
        # parse from ABC.txt in the song folder
        songObj.parseSong()

        # add song to songs list
        temp.append(songObj)

        # print the song object               for testing purposes
        print(songObj)
    return temp

def playGame():
    # start the game
    print("Start Game")
    # start the game
    game = Game(songs[0])
    game.startGame()

def main_menu():
    global songs
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Music Typing")
    clock = pygame.time.Clock()
    # light blue color
    screen.fill((173,216,230))

    menu = pygame_menu.Menu('Welcome', 1280, 720,
                       theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', playGame)
    menu.add.button("Refresh", refresh, songDir)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)
    
    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting")
                pygame.quit()
                raise SystemExit

        # update the display
        pygame.display.update()

if __name__ == "__main__":
    # global variables
    global song                                  # songs list
    mainDir = os.getcwd()                       # main directory
    songDir = mainDir + "\songs"                # song directory
    audioDir = mainDir + "\audio"               # audio directory (for if the audio file is not a youtube link)
    songs = refresh(songDir)
    # start the main menu
    main_menu()