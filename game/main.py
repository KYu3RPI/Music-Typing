from song import Song
from game import Game
import pygame
import os

# main
def main():
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Music Typing")
    clock = pygame.time.Clock()
    # light blue color
    screen.fill((173,216,230))

    # THIS WILL BE REPLACED A BUTTON ASSET!!!!
    # font
    font = pygame.font.Font('freesansbold.ttf', 32)
    # text
    starttext = font.render('Start', True, (160,160,160))
    refreshtext = font.render('Refresh', True, (160,160,160))
    # make start and refresh button
    startbutton = pygame.draw.rect(screen, (0,100,255), (100,100,100,50))
    refreshbutton = pygame.draw.rect(screen, (0,100,255), (100,200,150,50))
    # add text to button
    screen.blit(starttext, (110,110))
    screen.blit(refreshtext, (110,210))

    # get the current directory
    mainDir = os.getcwd()
    # get songs directory
    songDir = mainDir + "\songs"
    songs = []
    
    while True:
        # update the display
        pygame.display.update()

        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the button is clicked
                if startbutton.collidepoint(event.pos):
                    # start the game
                    print("Start Game")
                    # create game object
                    game = Game(songs[0])
                    # start the game
                    game.start()

                if refreshbutton.collidepoint(event.pos):
                    # refresh the songs list
                    songs = refresh(songDir)

        # on starup if songs is empty add song!!!!
        if (songs == []):
            songs = refresh(songDir)

def refresh(songDir):
    # clear songs list
    songs = []
    for song in os.listdir(songDir):
        # create song object
        songObj = Song(songDir + "\\" + song)
        # parse from ABC.txt in the song folder
        songObj.parseSong()

        # add song to songs list
        songs.append(songObj)

        # print the song object               for testing purposes
        songObj.printSong()
    return songs

main()