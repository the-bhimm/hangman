import pygame
import math
import random

# Set up the game window.
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# -----------------------------------------
#            GLOBAL VARIABLES
# -----------------------------------------
# Load in the images.
images = []
for i in range(12):
    image = pygame.image.load("assets/hangman"+str(i) + ".png")
    images.append(image)

# Create the buttons.
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A+i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("comicsans", 70)
SMALL_FONT = pygame.font.SysFont("comicsans", 30)

# Game variables.
hangman_status = 0
guessed = []
SCORE = 0
GUESS_REMAIN = 11
ROUND  = 1

# Colours
BLACK = 0, 0, 0
WHITE = 255, 255, 255

file = open("highscore.txt", "r")
HIGH_SCORE = file.read()

# -----------------------------------------
#               FUNCTIONS
# -----------------------------------------

# This is definitely not the best way to find the high score but I was experimenting with new techniques
# I'd learned and it works so I don't feel a need to change it now
def high_score(new_high):
    global HIGH_SCORE
    file = open("highscore.txt", "r")
    HIGH_SCORE = file.read()
    if int(HIGH_SCORE) < SCORE:
        file = open("highscore.txt", "w")
        file.write(str(new_high))

def random_word():
    file = open("wordlist.txt", "r")
    lines = file.readlines()
    wordlist = []
    for i in lines:
        i = i.strip("\n").upper()
        wordlist.append(i)
    i = random.choice(wordlist)
    return i


word = random_word()


def draw():
    win.fill(WHITE)
    # Draw title
    text4 = SMALL_FONT.render(f"Round: {ROUND}", 1, BLACK)
    win.blit(text4, (650, 5))
    text2 = SMALL_FONT.render(f"Score: {SCORE}", 1, BLACK)
    win.blit(text2, (650, 30))
    text3 = SMALL_FONT.render(f"Lives: {GUESS_REMAIN}", 1, BLACK)
    win.blit(text3, (70, 20))
    text = TITLE_FONT.render("Noah's Hangman", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 10))
    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
    # Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    global word
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    if hangman_status == 11:
        answer = word
        word = WORD_FONT.render(f"The answer was {answer}", 1, BLACK)
        win.blit(word, (WIDTH / 2 - word.get_width() / 2, 400))
    pygame.display.update()
    pygame.time.delay(3000)


def play_again():
    win.fill(WHITE)
    text2 = SMALL_FONT.render(f"Score: {SCORE}", 1, BLACK)
    win.blit(text2, (WIDTH / 2 - text2.get_width() / 2, 30))
    text = WORD_FONT.render("Would you like to continue?(y/n)", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()


def reset():
    global word
    global hangman_status
    global guessed
    global letters
    global GUESS_REMAIN
    global ROUND
    ROUND += 1
    RADIUS = 20
    GAP = 15
    letters = []
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 400
    A = 65
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
    GUESS_REMAIN = 11
    guessed = []
    hangman_status = 0
    word = random_word()
    high_score(SCORE)
    draw()


def check_pressed():
    global play
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                reset()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    play = False


def main():
    global hangman_status
    global play
    global SCORE
    global GUESS_REMAIN
    fps = 144
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(fps)

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
                                GUESS_REMAIN -= 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            SCORE += 1
            pygame.time.delay(1000)
            display_message("You won!")
            play_again()
            pygame.time.delay(5000)
            check_pressed()
            break

        if hangman_status == 11:
            pygame.time.delay(1000)
            display_message("You lost!")
            play_again()
            pygame.time.delay(5000)
            check_pressed()
            break


play = True
while play:
    main()
else:
    pygame.quit()

