import pygame
import random
import math

from pygame import mixer

#initialize
pygame.init()

#create screen
screen=pygame.display.set_mode((800,600))

#background 
background = pygame.image.load('background.png')

#background music
mixer.music.load('bgmusic.wav')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('science-fiction.png')
pygame.display.set_icon(icon)

#players
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 520
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(5)
    enemyY_change.append(40)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 520
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score_value
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',65)

def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255,255,255))
    screen.blit(over_text, (200,250))


def show_score(x,y):
    score = font.render("Score: " + str(score_value),True,(0,255,0))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance <= 27:
        return True
    else:
        return False

#game loop
running= True
while running:

    #rgb color
    screen.fill((0, 0, 0))

    #background
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
              #  print("left arrow pressed")
                playerX_change = -3
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
               # print("right arrow pressed")
                playerX_change = 3
                
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
               # print("Keystroke released")
                playerX_change = 0

    # player movement
    playerX += playerX_change 

    if playerX <=0:
        playerX = 0
    elif playerX >=736:
        playerX = 736
    
    #enemy movement
    for i in range(num_of_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()   
            break
        
        enemyX[i] += enemyX_change[i] 

        if enemyX[i] <= 0:
            enemyX_change[i] = random.randint(4,7)
            enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >= 736:
            enemyX_change[i] = random.randint(-7,-4)
            enemyY[i] += enemyY_change[i]
        
        #collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()

        enemy(enemyX[i],enemyY[i],i)

        
    #bullet movement
    if bulletY <= 0:
        bulletY = 520
        bullet_state = "ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
   
    player(playerX,playerY)

    show_score(textX,textY)

    pygame.display.update()