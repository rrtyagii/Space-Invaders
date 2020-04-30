import math
import pygame
import random
from pygame import mixer

# initializing the pygame
pygame.init()
# pygame.mixer.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space-game.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('spaceship.png')
player_X = 255
player_Y = 520
player_X_change = 0
player_Y_change = 0

# Enemy / Alien
enemy_image = pygame.image.load('alien.png')
enemy_X = 255
enemy_Y = 52
enemy_y_change = 20
enemy_x_change = 5.3

# Background and Background sound
background = pygame.image.load("background1.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

# Bullet
bullet_image = pygame.image.load("bullet.png")
bullet_state = 'ready'  # ready state = you can't see bullet
# fire = the bullet is currently moving
bullet_X = 0
bullet_Y = 520
bullet_X_change = 0
bullet_Y_change = 12

# score = 0

score_value = 0
font = pygame.font.Font("ParryHotter.ttf", 32)

textX = 10
textY = 10

# Game Over
game_over = pygame.font.Font("ParryHotter.ttf", 64)


def game_over_text():
    gameOver = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameOver, (399, 299))


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_image, (int(x), int(y)))


def enemy(x, y):
    screen.blit(enemy_image, (int(x), int(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_image, (int(x + 16), int(y + 10)))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


def colide_player_enemy(enemyX, enemyY, playerX, playerY):
    colideDistance = math.sqrt((math.pow((enemyX - playerX), 2)) + (math.pow((enemyY - playerY), 2)))
    if colideDistance < 20:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB -Red, Green, Blue
    screen.fill((255, 155, 245))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            # print('A keystroke has pressed')
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                player_X_change = -5.1

            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                player_X_change = 5.1

            if event.key == pygame.K_UP:
                # print("Up arrow is pressed")
                player_Y_change = -5

            if event.key == pygame.K_DOWN:
                # print("Down arrow is pressed")
                player_Y_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_X = player_X
                    bullet_Y = player_Y
                    fire_bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                # print('Keystroke has been released')
                player_X_change = 0
                player_Y_change = 0

    # Player Movement
    player_X += player_X_change

    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736

    player_Y += player_Y_change
    if player_Y <= 380:
        player_Y = 380
    elif player_Y >= 536:
        player_Y = 536

    #    enemy(enemy_X-10 , enemy_Y)
    # enemy(enemy_X+100, enemy_Y)
    # enemy(enemy_X-200 , enemy_Y)
    # enemy(enemy_X+200, enemy_Y)
    # enemy(enemy_X, enemy_Y+100)
    # enemy(enemy_X-100 , enemy_Y+100)
    # enemy(enemy_X+100, enemy_Y+100)
    # enemy(enemy_X-200 , enemy_Y+100)
    # enemy(enemy_X+200, enemy_Y+100)

    # Enemy Movement

    ##Game Over
    playerColide = colide_player_enemy(enemy_X, enemy_Y, player_X, player_Y)
    if playerColide:
        enemy_Y = 599
        game_over_text()

    enemy_X += enemy_x_change
    if enemy_X <= 0:
        enemy_x_change = 5.3
        enemy_Y += enemy_y_change
    elif enemy_X >= 736:
        enemy_x_change = -5.3
        enemy_Y += enemy_y_change

    # Bullet Movement
    if bullet_Y <= 0:
        bullet_Y = 520
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_change

    # Collision Detection
    collision = isCollision(enemy_X, enemy_Y, bullet_X, bullet_Y)
    if collision:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        bullet_Y = 520
        bullet_state = "ready"
        score_value += 1
        enemy_X = random.randint(0, 735)
        enemy_Y = random.randint(0, 380)

    player(player_X, player_Y)
    enemy(enemy_X, enemy_Y)
    show_score(textX, textY)

    pygame.display.update()
