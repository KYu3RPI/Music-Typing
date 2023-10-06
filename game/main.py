from song import Song
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Music Typing")
clock = pygame.time.Clock()
mainDir = os.getcwd()
# go back one directory
songDir = mainDir + "\songs"

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            pygame.quit()
            raise SystemExit
    
    # BASIC CODE RIGHT NOW, WILL IMPORT ALL THE SONGS IN THE SONG FOLDER LATER

    # create song object
    song = Song(songDir + "\ABC.txt")
    # parse from ABC.txt in the song folder
    song.parseSong()
    # print the song object
    song.printSong()