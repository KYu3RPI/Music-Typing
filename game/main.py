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
songs = []

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            pygame.quit()
            raise SystemExit
    
    # BASIC CODE RIGHT NOW, WILL IMPORT ALL THE SONGS IN THE SONG FOLDER LATER

    # on starup if songs is empty add song!!!!
    if (not songs):
        for song in os.listdir(songDir):
            # create song object
            songObj = Song(songDir + "\\" + song)
            # parse from ABC.txt in the song folder
            songObj.parseSong()
            # print the song object
            songObj.printSong()
            # add song to songs list
            songs.append(songObj)