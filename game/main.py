from song import Song
from game import Game
import pygame
import pygame_menu
import os

def close():
    print("Quitting")
    pygame.quit()
    raise SystemExit

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
    game = Game(songs[0])

    # start the display of the game
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Music Typing")
    clock = pygame.time.Clock()

    audio = game.getSongAudio()

    while True:
        screen.fill(game.getSong().getBackgroundFile())
        # button to go back to main
        backbuttonPosition = (1180,25,100,50)
        backbutton = pygame.draw.rect(screen, (0,150,200), backbuttonPosition)
        font = pygame.font.Font('freesansbold.ttf', 32)
        # text
        backtext = font.render('Back', True, (255,255,255))
        # add text to button
        screen.blit(backtext, (backbutton[0] + 10, backbutton[1] + 10))

        # rest of ui
        # title of song
        title = font.render(game.getSong().getTitle(), True, (255,255,255))
        screen.blit(title, (25,25))
        # score information
        cWPM = game.getCurrentWPM()
        aWPM = game.getAvgWPM()
        acc = game.getAccuracy()
        score = game.getScore()
        score = font.render(f"Current WPM: {cWPM:.2f} | Average WPM: {aWPM:.2f} | Accuracy: {acc:.0%} | Score: {score}", True, (255,255,255))
        screen.blit(score, (25,660))

        #get lines
        previousLine = font.render(game.getPreviousLyric(), True, (192,239,255))
        line = font.render(game.getCurrentLyric(), True, (255,255,255))
        nextLine = font.render(game.getNextLyric(), True, (117,146,156))

        # get typed line
        typedLine = font.render(game.getTypedLyric(), True, (0,0,0))
        mistakes = font.render(game.getTypedLyric() + game.getMistakes() + "_", True, (255,0,0))

        screen.blit(previousLine, (25, 100))
        screen.blit(line, (25, 150))
        screen.blit(nextLine, (25, 200))
        screen.blit(mistakes, (25, 150))
        screen.blit(typedLine, (25, 150))

        pygame.display.update()

        # play the music
        if audio != None:
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()

        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the button is clicked
                if backbutton.collidepoint(event.pos):
                    # go back to main
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    print("Back to Main")
                    return
            if event.type == pygame.KEYDOWN:
                # if the key is pressed
                # check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # check if there are mistakes to delete
                    if len(game.getMistakes()) > 0:
                        # delete the last mistake
                        game.backspace()
                        continue

                else:
                    # catch every letter that the player is typing
                    # check for capital letters
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        continue
                    cont = game.typeLetter(event.unicode)
                    if cont == 1:
                        print("Next Line")
                    if cont == -1:
                        print("Song Over")
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        return

def main_menu():
    global songs
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Music Typing")
    clock = pygame.time.Clock()

    mytheme = pygame_menu.themes.THEME_BLUE.copy()
    mytheme.background_color=(173,216,230)
    mytheme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    mytheme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    menu = pygame_menu.Menu('Music Typing', 1280, 720, theme=mytheme)
    menu.add.button('Play', playGame)
    menu.add.button("Refresh", refresh, songDir)
    menu.add.button('Quit', close)

    menu.mainloop(screen)
    
    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

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