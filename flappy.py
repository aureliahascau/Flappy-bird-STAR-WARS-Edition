import pygame, sys, random

pygame.init()

pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
window = pygame.display.set_mode((500,700))   #dimensiunile alese astfel incat imaginea
                                             #de fundal sa fie jumatate din acestea  
img_surface = pygame.image.load('img/mobile.jpg')  

ship_surface = pygame.image.load('img/spaceship.png') 
ship_rect = ship_surface.get_rect(center = (150, 450))

# Different images for the asteroids

asteroid_images = []
asteroid_list = []

ast_surface1 = pygame.transform.scale(pygame.image.load("asteroid1.png"), (100, 100))
ast_surface2 = pygame.transform.scale(pygame.image.load("asteroid2.png"), (100, 100))
ast_surface3 = pygame.transform.scale(pygame.image.load("asteroid3.png"), (120, 120))

asteroid_images.append(ast_surface1)
asteroid_images.append(ast_surface2)
asteroid_images.append(ast_surface3)

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

# Collision system

# def check_for_crash(asteroids):
#     for asteroid_tuple in asteroids:
#         if ship_rect.colliderect(asteroid_tuple[0]):
#             print('collision')

# Movement on the y axis for the spaceshit

ship_position = 0
gravity = 0.05

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
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship_position = 0
                ship_position -= 3

        # Spawning asteroird every 1.1 seconds
        
        if event.type == SPAWNOBSTACLE:
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

    window.blit(pygame.transform.scale(ship_surface, (80, 60)), ship_rect)
    # check_for_crash(asteroid_list)

    # Spaceship movement on Y axis

    ship_position += gravity
    ship_rect.centery += ship_position

    # Generating and drawing asteroids

    asteroid_list = move_asteroid(asteroid_list)
    
    draw_asteroid(asteroid_list)

    pygame.display.update()

    clock.tick(90)  


#pentru a pune pipe-uri se creeaza o lista de rectangles 
# se creeaza o a 2 a lista ce contine toate inaltimile posibile ale pipe urilor
# din lista se vor lua cu random
# pt a da flip la surface : pygame.transform.flip(surface,False,True) - flip pe y
# pt rotatie : pygame.transform.rotozoom(surface, unghiul cu care vrem sa facem rotatia,1)


