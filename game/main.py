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

def endMenu(game):
    # result screen when game is over
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Music Typing")

    # get information about game
    songname = game.getSong().getTitle()
    score = game.getScore()
    avgWPM = game.getAvgWPM()
    accuracy = game.getAccuracy()
    totalTyped = game.getTotalLetters()


def playGame():
    # start the game
    print("Start Game")
    game = Game(songs[0])

    # start the display of the game
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Music Typing")

    audio = game.getSongAudio()
    
    setup = True
    starttime = 0
    timercont = 1
    typecont = 1

    while True:
        if setup:
            # get the start time
            starttime = pygame.time.get_ticks()
            # play the music
            if audio != None:
                pygame.mixer.music.load(audio)
                pygame.mixer.music.play()

        screen.fill(game.getSong().getBackgroundFile())
        # button to go back to main
        backbuttonPosition = (1180,25,100,50)
        backbutton = pygame.draw.rect(screen, (0,150,200), backbuttonPosition)
        mainfont = pygame.font.Font('freesansbold.ttf', 32)
        gamefont = pygame.font.Font('freesansbold.ttf', 48)
        # text
        backtext = mainfont.render('Back', True, (255,255,255))
        # add text to button
        screen.blit(backtext, (backbutton[0] + 10, backbutton[1] + 10))

        # rest of ui
        # title of song
        title = mainfont.render(game.getSong().getTitle(), True, (255,255,255))
        screen.blit(title, (25,25))
        # score information
        cWPM = game.getCurrentWPM()
        aWPM = game.getAvgWPM()
        acc = game.getAccuracy()
        score = game.getScore()
        score = mainfont.render(f"Current WPM: {cWPM:.2f} | Average WPM: {aWPM:.2f} | Accuracy: {acc:.0%} | Score: {score:.2f}", True, (255,255,255))
        screen.blit(score, (25,660))

        # check if it is past start time
        if pygame.time.get_ticks() - starttime >= game.getCurrentStanzaStart() * 1000:
            # check if time is up for current stanza
            if typecont == -1:
                print("Song Over")
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                return
            
            if pygame.time.get_ticks() - starttime >= game.getNextStanzaStart() * 1000:
                # if it is then go to the next stanza
                timercont = game.nextStanza()
                if timercont == 1:
                    print("Next Stanza")
                if timercont == -1: # last stanza
                    print("Song Time Over")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    return

            #get lines
            previousLine = gamefont.render(game.getPreviousLyric(), True, (192,239,255))
            line = gamefont.render(game.getCurrentLyric(), True, (255,255,255))
            nextLine = gamefont.render(game.getNextLyric(), True, (117,146,156))

            # get typed line
            typedLine = gamefont.render(game.getTypedLyric(), True, (0,0,0))
            mistakes = gamefont.render(game.getTypedLyric() + game.getMistakes(), True, (255,0,0))
            cursor = gamefont.render(game.getTypedLyric() + game.getMistakes() + "_", True, (0,0,0))

            screen.blit(previousLine, (25, 100))
            screen.blit(line, (25, 150))
            screen.blit(nextLine, (25, 200))
            screen.blit(cursor, (25, 150))
            screen.blit(mistakes, (25, 150))
            screen.blit(typedLine, (25, 150))

            pygame.display.update()

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
                        typecont = game.typeLetter(event.unicode)
                        if typecont == 1:
                            print("Next Line")
                            # delay the line until the next stanza starts
                        if typecont == -1:
                            print("Song Typing Over")

        pygame.display.update()

        if pygame.time.get_ticks() - starttime < game.getCurrentStanzaStart() * 1000:
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
        setup = False

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
    if len(songs) == 1:
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