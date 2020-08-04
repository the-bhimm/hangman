import pygame
import math
import random

#Set up the game window.
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

#Load in the images.
images = []
for i in range(12):
    image = pygame.image.load("hangman"+str(i) + ".png")
    images.append(image)

#Create the buttons.
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i%13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A+i), True])

#Fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("comicsans", 70)
SMALL_FONT = pygame.font.SysFont("comicsans", 30)

#Game variables.
hangman_status = 0
file = open("wordlist.txt", "r")
lines = file.readlines()
wordlist = []
for i in lines:
    i = i.strip("\n").upper()
    wordlist.append(i)
word = random.choice(wordlist)
guessed = []

#Colours
BLACK = 0, 0, 0
WHITE = 255, 255, 255


def draw():
    win.fill(WHITE)
    #Draw title
    text = TITLE_FONT.render("Noah's Hangman", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 10))


    #Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    #Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x,y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2,y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def display_message(message):
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

def play_again():
    win.fill(WHITE)
    text2 = SMALL_FONT.render("Window will close automatically if nothing is pressed", 1, BLACK)
    win.blit(text2, (WIDTH / 2 - text2.get_width() / 2, 30))
    text = WORD_FONT.render("Click here to play again", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    global hangman_status
    global play

    FPS = 144
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x-m_x)**2 + (y-m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            pygame.time.delay(1000)
            display_message("You won!")
            play_again()
            break

        if hangman_status == 11:
            pygame.time.delay(1000)
            display_message("You lost!")
            play_again()
            break


play = True
while play:
    print(word) #for testing purposes so I can get a victory
    main()
else:
    print("Play is now false")
    pygame.quit()
