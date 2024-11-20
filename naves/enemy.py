import random
import pygame
import globals
from constants import *

ORIGINAL_SIZE = (512, 512)
MIN_WIDTH = 15
MAX_WIDTH = 80

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()

        self.width = random.randint(MIN_WIDTH, MAX_WIDTH)
        self.height = (self.width / ORIGINAL_SIZE[0]) * ORIGINAL_SIZE[1]

        self.surf = pygame.image.load('naves/img/10.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.surf)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, ancho_ventana), 
                random.randint(-100, -20)
            )
        )
        
       
        self.speed = (random.randint(1, 3) / 10) * (1 + ((globals.game_speed)*3.14 / 5/56))

    def update(self, delta_time):
        self.rect.move_ip(0, self.speed * delta_time)
        self.mask = pygame.mask.from_surface(self.surf)
        
       
        if self.rect.top > alto_ventana: 
            self.kill()
