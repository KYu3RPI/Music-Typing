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
    global songs
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
    songs = temp

def set_Song(value, num):
    global songs
    global index
    index = num
    if index < 0:
        index = 0
    if index >= len(songs):
        index = len(songs) - 1
    song = songs[index].getTitle()

def result(game):
    # result screen when game is over
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Music Typing")
    backbuttonPosition = (1180,25,100,50)
    backbutton = pygame.draw.rect(screen, (0,150,200), backbuttonPosition)
    mainfont = pygame.font.Font('freesansbold.ttf', 32)
    titlefont = pygame.font.Font('freesansbold.ttf', 48)
    backtext = mainfont.render('Back', True, (255,255,255))
    screen.blit(backtext, (backbutton[0] + 10, backbutton[1] + 10))

    # title of song
    title = titlefont.render(game.getSong().getTitle(), True, (255,255,255))
    text_rect = title.get_rect(center=(1280/2, 720 - 600))
    screen.blit(title, text_rect)

    # get information about game
    songname = game.getSong().getTitle()
    score = game.getScore()
    avgWPM = game.getAvgWPM()
    accuracy = game.getAccuracy()
    totalTyped = game.getTotalLetters()

    # display information
    pygame.display.update()
    
    while True:

        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the button is clicked
                if backbutton.collidepoint(event.pos):
                    # go back to main
                    print("Back to Main")
                    return

def playGame():
    global index
    # start the game
    print("Start Game")
    game = Game(songs[index])

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
                result(game)
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
                    result(game)
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
                        if event.unicode == "":
                            continue
                        typecont = game.typeLetter(event.unicode, pygame.time.get_ticks()/1000.0 - game.getCurrentStanzaStart())
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
    global index
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
    menu.add.selector('Song: ', [(songs[i].getTitle(), i) for i in range(len(songs))], onreturn=playGame, onchange=set_Song)
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
    global songs                                # songs list
    mainDir = os.getcwd()                       # main directory
    songDir = mainDir + "\songs"                # song directory
    audioDir = mainDir + "\audio"               # audio directory (for if the audio file is not a youtube link)
    refresh(songDir)
    global index
    # start the main menu
    main_menu()