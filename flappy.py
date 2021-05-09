import pygame, sys, random

pygame.init()

pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
window = pygame.display.set_mode((500,700))   
                                               

img_surface = pygame.image.load('img/mobile.jpg')

game_font = pygame.font.Font('flappy_font.TTF', 26)
game_font2 = pygame.font.Font('flappy_font.TTF', 35)

ship_surface = pygame.image.load('img/spaceship.png') 
ship_rect = ship_surface.get_rect(center = (150, 450))

ship_rect = pygame.Rect((30, 350), (80, 60))
sound = pygame.mixer.Sound('mars.wav')


# Different images for the asteroids

asteroid_images = []
asteroid_list = []

ast_surface1 = pygame.transform.scale(pygame.image.load("asteroid1.png"), (100, 100))
ast_surface2 = pygame.transform.scale(pygame.image.load("asteroid2.png"), (100, 100))
ast_surface3 = pygame.transform.scale(pygame.image.load("asteroid3.png"), (100, 100))

asteroid_images.append(ast_surface1)
asteroid_images.append(ast_surface2)
asteroid_images.append(ast_surface3)

score = 0
high_score=0

def create_asteroid(positionY):
    selected_asteroid = random.choice(asteroid_images)
    asteroid = selected_asteroid.get_rect(midtop = (800, positionY))
    return (asteroid, selected_asteroid)

def move_asteroid(asteroids):
    for asteroid_tuple in asteroids:
        asteroid_tuple[0].centerx -= 3.5
    return asteroids

def draw_asteroid(asteroids):
    for asteroid_tuple in asteroids:
        window.blit(asteroid_tuple[1], asteroid_tuple[0])

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (250, 50))
        window.blit(score_surface, score_rect)
        
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


def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score


# Movement on the y axis for the spaceshit

ship_position = 0
gravity = 0.05



MENU = True

SPAWNOBSTACLE = pygame.USEREVENT

pygame.time.set_timer(SPAWNOBSTACLE, 1100)


def get_rand_position():
    pos1 = random.randint(100, 600)
    pos2 = random.randint(100, 600)

    while abs(pos1 - pos2) < 150:
        pos1 = random.randint(100, 600)
    
    return (pos1, pos2)

while True:
    for event in pygame.event.get():
        sound.play()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and MENU == False:
                ship_position = 0
                ship_position -= 3
            if event.key == pygame.K_SPACE and MENU == True:
                MENU = False
                asteroid_list.clear()
                ship_rect.centery = 350
                ship_position = 0
                ship_position -= 3
                score=0

        # Spawning asteroird every 1.1 seconds
        
        if event.type == SPAWNOBSTACLE and MENU == False:
            number_of_asteroids = random.randint(1, 3)
            if number_of_asteroids == 1:
                asteroid_list.append(create_asteroid(random.randint(100, 600)))
            else:
                position = get_rand_position()

                asteroid_list.append(create_asteroid(position[0]))
                asteroid_list.append(create_asteroid(position[1]))

    # Loading background

    window.blit(pygame.transform.scale(img_surface, (500, 700)), (0, 0))

    # Drawing the spaceship

    
    check_for_crash(asteroid_list)

    if MENU == False:
        window.blit(pygame.transform.scale(ship_surface, (80, 60)), ship_rect)
        # Spaceship movement on Y axis

        ship_position += gravity
        ship_rect.centery += ship_position

        # Generating and drawing asteroids

        asteroid_list = move_asteroid(asteroid_list)
        
        draw_asteroid(asteroid_list)

        if check_for_crash(asteroid_list):
            MENU = True

        # Getting score and high score

        score += 0.01
        score_display('main_game')
    else:
        draw_asteroid(asteroid_list)
        game_surface = game_font2.render("Get ready!", True, (255,0,0))
        game_rect = game_surface.get_rect(center = (250, 350))
        window.blit(game_surface, game_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        

    pygame.display.update()

    clock.tick(100)  




