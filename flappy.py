#!/usr/bin/env python3

import pygame, sys, random

pygame.init()
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
window=pygame.display.set_mode((500,700))   #dimensiunile alese astfel incat imaginea
                                             #de fundal sa fie jumatate din acestea  
img_surface=pygame.image.load('img/mobile.jpg')   
ship_surface=pygame.image.load('img/space.png') 

while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
    window.blit(pygame.transform.scale(img_surface, (500, 700)), (0, 0))
    window.blit(pygame.transform.scale(ship_surface, (100, 100)), (0, 0))
    pygame.display.update()

    clock.tick(100)  #trebuie sa fie >30


#pentru a pune pipe-uri se creeaza o lista de rectangles 
# se creeaza o a 2 a lista ce contine toate inaltimile posibile ale pipe urilor
# din lista se vor lua cu random
# pt a da flip la surface : pygame.transform.flip(surface,False,True) - flip pe y
# pt rotatie : pygame.transform.rotozoom(surface, unghiul cu care vrem sa facem rotatia,1)


