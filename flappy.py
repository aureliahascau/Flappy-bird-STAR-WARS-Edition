import pygame, sys, random

pygame.init()

pygame.display.set_caption('Flappy Bird, STAR WARS Edition')
clock = pygame.time.Clock()
window = pygame.display.set_mode((500,700))   

# Background
                                              
img_surface = pygame.image.load('img/mobile.jpg')
background_image = pygame.transform.scale(img_surface, (500, 700))

# Fonts

game_font = pygame.font.Font('flappy_font.TTF', 26)
game_font2 = pygame.font.Font('flappy_font.TTF', 35)

# Ship's image and hitbox

ship_surface = pygame.image.load('img/spaceship.png')
ship_rect = ship_surface.get_rect(center = (150, 450))
ship_rect = pygame.Rect((30, 350), (80, 60))
ship_image = pygame.transform.scale(ship_surface, (80, 60))

# Background sound

background_music = pygame.mixer.Sound('sounds/mars.wav')
background_music.set_volume(1.0)

# Explosion image & sound

exp_surface = pygame.transform.scale(pygame.image.load('img/explosion.png'),(120, 160))
exp_sound = pygame.mixer.Sound('sounds/explosion.wav')
exp_sound.set_volume(0.75)

# Creating 3 types of asteroids 

asteroid_images = []
asteroid_list = []

ast_surface1 = pygame.transform.scale(pygame.image.load("img/asteroid1.png"), (100, 100))
ast_surface2 = pygame.transform.scale(pygame.image.load("img/asteroid2.png"), (100, 100))
ast_surface3 = pygame.transform.scale(pygame.image.load("img/asteroid3.png"), (100, 100))

asteroid_images.append(ast_surface1)
asteroid_images.append(ast_surface2)
asteroid_images.append(ast_surface3)

# Asteroid functions

def create_asteroid(positionY):
    selected_asteroid = random.choice(asteroid_images)
    asteroid = selected_asteroid.get_rect(midtop = (800, positionY))
    return (asteroid, selected_asteroid) # Returing tuple of the asteroid and it's image

def move_asteroid(asteroids):
    for asteroid_tuple in asteroids:
        asteroid_tuple[0].centerx -= 3.5
    return asteroids

def draw_asteroid(asteroids):
    for asteroid_tuple in asteroids:
        window.blit(asteroid_tuple[1], asteroid_tuple[0])

def remove_asteroid(asteroids):
    i = 0
    for asteroid in asteroids:
        if asteroid[0].centerx < -100:
            del asteroids[i]
        i += 1

# Function to make sure that two asteroids don't spawn in the same place

def get_rand_position(): 
    pos1 = random.randint(100, 600)
    pos2 = random.randint(100, 600)

    while abs(pos1 - pos2) < 150: # Distance between two asteroids must be bigger than 150
        pos1 = random.randint(100, 600)
    
    return (pos1, pos2)

# Displaying score functions

def score_display(game_state):

    # While playing the game, only current score is displayed

    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (250, 50))
        window.blit(score_surface, score_rect)
        
    # Displays score and the high score when in game menu

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (250, 50))
        window.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (250, 650))
        window.blit(high_score_surface, high_score_rect)

# Collision system

def check_for_crash(asteroids):
    for asteroid_tuple in asteroids:
        if ship_rect.colliderect(asteroid_tuple[0]):
            return True

    if ship_rect.top <= 0 or ship_rect.bottom >= 700:
        return True

    return False

# Scoring system

score = 0
high_score = 0

def add_points(asteroids):
    local_score = 0
    for asteroid in asteroids:
        if asteroid[0].centerx < 30 and asteroid[0].centerx > 25:
            local_score += 1
    return local_score

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

# Player gets one point every time the ship passes an asteroid

def explosion_position(hitbox):
    explosion_rect = pygame.Rect((hitbox.left + 15, hitbox.top - 50), (80, 80))
    return explosion_rect

# Movement on the y axis for the spaceshit

ship_position = 0
gravity = 0.05

MENU = True
FIRST_TIME_OPENED = True

# Generating an asteroid is an event

SPAWNOBSTACLE = pygame.USEREVENT

pygame.time.set_timer(SPAWNOBSTACLE, 1100)

pygame.mixer.Channel(0).play(background_music)

while True:

    pygame.display.update()
    clock.tick(100) # Tickrate

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Allows the game to be closed using 'X'
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and MENU == False: # Spaceship going up and while playing the game
                ship_position = 0
                ship_position -= 3
                
            if event.key == pygame.K_SPACE and MENU == True: # Exits the main menu, makes the first move and clears all objects 
                MENU = False
                asteroid_list.clear()
                ship_rect.centery = 350
                ship_position = 0
                ship_position -= 3
                score = 0
    
        # Spawning asteroird every 1.1 seconds
        
        if event.type == SPAWNOBSTACLE and MENU == False:
            number_of_asteroids = random.randint(1, 3) # 1 in 3 chance to spawn 2 asteroids in the same line
            if number_of_asteroids == 1:
                position = get_rand_position()
                asteroid_list.append(create_asteroid(position[0]))
                asteroid_list.append(create_asteroid(position[1]))             
            else:
                asteroid_list.append(create_asteroid(random.randint(100, 600)))

                

    # Loading background

    window.blit(background_image, (0, 0))

    if MENU == False: # While game is running

        # Loading ship

        window.blit(ship_image, ship_rect)

        # Spaceship movement on Y axis

        ship_position += gravity
        ship_rect.centery += ship_position

        # Generating and drawing asteroids

        asteroid_list = move_asteroid(asteroid_list)
        
        draw_asteroid(asteroid_list)
        remove_asteroid(asteroid_list)

        # Crash detection

        if check_for_crash(asteroid_list): # Upon crashing, the game directs you to the main menu
            MENU = True
            FIRST_TIME_OPENED = False
            pygame.mixer.Channel(1).play(exp_sound)
            
        # Getting current score

        score += add_points(asteroid_list)

        score_display('main_game')
    
    else: # While in game menu

        # Draw ship and asteroids when losing the game

        draw_asteroid(asteroid_list)
        window.blit(ship_image, ship_rect)

        if FIRST_TIME_OPENED == True:
            game_surface = game_font2.render("Get ready!", True, (255,0,0)) # Greeting message when you enter the game 
        else:
            game_surface = game_font2.render("You lost!", True, (255,0,0)) # Game message when you lose
            window.blit(exp_surface, explosion_position(ship_rect)) # When a crash is detected, an explosion appears

        # The score and high score are always displayed while in game menu

        game_rect = game_surface.get_rect(center = (250, 350))
        window.blit(game_surface, game_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')




