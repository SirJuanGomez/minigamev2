import pygame
from pygame.locals import *
import globals
from constants import *
import random

WIDTH=48
HEIGHT=48

ASSET_SIZE = 24

class Money(pygame.sprite.Sprite):
    def __init__(self):
        super(Money, self).__init__()

        self.current_animation = "idle"
        self.animations = {}
        self.animation_behaviour = {
            "idle": "continuous"
        }

        self.load_assets()

        self.idxAnimation = 0
        self.animationSpeed = .15
        self.surf = self.animations[self.current_animation][self.idxAnimation]
        self.surf = pygame.transform.scale(self.surf, (WIDTH,HEIGHT))
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(
            ancho_ventana, 
            random.randrange(int(alto_ventana*.5), int(ancho_ventana*.8))
        )
        self.speed = random.randrange (2,4) / 10


    def load_assets(self):
        self.animations["idle"] = []
        asset = pygame.image.load("plataformas/img/4 Animated objects/Card.png").convert_alpha()
        width = asset.get_width()
        idx = 0
        while (idx*ASSET_SIZE < width):
            frame = pygame.Surface((ASSET_SIZE, ASSET_SIZE), pygame.SRCALPHA)
            frame.blit(asset, asset.get_rect(), Rect(idx*ASSET_SIZE, 0, ASSET_SIZE, ASSET_SIZE))
            self.animations["idle"].append(
                frame.convert_alpha()
            )
            idx+=1


    def animate(self,delta_time):
        self.animationSpeed = .008 * delta_time
        self.idxAnimation += self.animationSpeed
        if int(self.idxAnimation)+1 >= len(self.animations[self.current_animation]):
            if self.animation_behaviour[self.current_animation] == "continuous":
                self.idxAnimation = 0
            else:
                self.idxAnimation = len(self.animations[self.current_animation])-1
        self.surf = self.animations[self.current_animation][int(self.idxAnimation)]
        self.surf = pygame.transform.scale(self.surf, (WIDTH,HEIGHT))
        self.rect = self.surf.get_rect()

    def update(self, delta_time):
        self.animate(delta_time)
        self.pos.x -= self.speed * globals.game_speed * delta_time
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

        if (self.rect.x + WIDTH) < 0:
            self.kill()

    #Llamar para mostrar el hitbox (debug)
    def display_hitbox(self, dest):
        debugRect = pygame.Surface((self.rect.width,self.rect.height))
        debugRect.set_alpha(128)
        debugRect.fill((0,255,0))
        pygame.display.get_surface().blit(debugRect, (self.rect.x, self.rect.y))