import pygame
from pygame.locals import *
import globals
from constants import *
import random

ancho=80
alto=80

asset_size=32

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.current_animation = "walk"
        self.animations = {}
        self.animation_behaviour = {
            "walk": "continuous"
        }

        self.load_assets()

        self.idxAnimation = 0
        self.animationSpeed = .15
        self.surf = self.animations[self.current_animation][self.idxAnimation]
        self.surf = pygame.transform.scale(self.surf, (ancho,alto))
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(
            ancho_ventana, 
            random.randrange(int(alto_ventana*.5), int(alto_ventana*.8))
        )
        self.speed = random.randrange (2,4) / 10
        self.update_mask()

    def load_assets(self):
        self.animations["walk"] = []
        asset = pygame.image.load("plataformas/img/7 Bird/Walk.png").convert_alpha()
        asset = pygame.transform.flip(asset,flip_x=90,flip_y=0)
        width = asset.get_width()
        idx = 0
        while (idx*asset_size < width):
            frame = pygame.Surface((asset_size, asset_size), pygame.SRCALPHA)
            frame.blit(asset, asset.get_rect(), Rect(idx*asset_size, 0, asset_size, asset_size))
            self.animations["walk"].append(
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
        self.surf = pygame.transform.scale(self.surf, (ancho,alto))
        self.surf= pygame.transform.rotate(self.surf,15)
        self.rect = self.surf.get_rect()

    #Solo moverlo a la izquierda segun la velocidad, etc
    def update(self, delta_time):
        self.animate(delta_time)
        self.pos.x -= self.speed * globals.game_speed * delta_time
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

        if (self.rect.x + ancho) < 0:
            self.kill()
        self.update_mask()

    #Colision se hace con mascaras, con el 90% del tamano del sprite
    def update_mask(self):
        self.maskSurface = self.surf
        self.maskSurface = pygame.transform.scale(self.maskSurface, (ancho*.9,alto*.9))
        self.mask = pygame.mask.from_surface(self.maskSurface)