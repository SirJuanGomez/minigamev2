import pygame
from constants import *
import globals
import random

platform_height=64
tile_width=64
tile_height=64

class GamePlatform(pygame.sprite.Sprite):
    def __init__(self, tileNumber, x):
        super(GamePlatform, self).__init__()

        width = tileNumber * tile_width
        self.height = random.randint(16,256)
        self.surf = pygame.Surface((width, self.height), pygame.SRCALPHA)

        tiles = []
        #Primer Tipo Plataforma 
        tiles.append({
            "unique": "Tile_30.png",
            "beginning": "Tile_01.png",
            "middle": "Tile_02.png",
            "end": "Tile_03.png",
            "beginning_bottom": "Tile_24.png",
            "middle_bottom": "Tile_24.png",
            "end_bottom": "Tile_24.png"
        })
        #Plataforma Flotante
        tiles.append({
            "unique": "Tile_47.png",
            "beginning": "Tile_44.png",
            "middle": "Tile_45.png",
            "end": "Tile_46.png"
        })
        #Segundo Tipo Plataforma 
        tiles.append({
            "unique": "Tile_30.png",
            "beginning": "Tile_21.png",
            "middle": "Tile_22.png",
            "end": "Tile_23.png",
            "beginning_bottom": "Tile_65.png",
            "middle_bottom": "Tile_65.png",
            "end_bottom": "Tile_65.png"
        })
        
        #Tomar un indice randomio
        tile_idx = random.randrange(len(tiles))

        platformImageSurf_unique = pygame.image.load("plataformas/img/1_Tiles/" + tiles[tile_idx]["unique"]).convert_alpha()
        platformImageSurf_beginning = pygame.image.load("plataformas/img/1_Tiles/" + tiles[tile_idx]["beginning"]).convert_alpha()
        platformImageSurf_middle = pygame.image.load("plataformas/img/1_Tiles/" + tiles[tile_idx]["middle"]).convert_alpha()
        platformImageSurf_end = pygame.image.load("plataformas/img/1_Tiles/" + tiles[tile_idx]["end"]).convert_alpha()
        platformImageSurf_beginning_bottom = None
        platformImageSurf_middle_bottom = None
        platformImageSurf_end_bottom = None


        if "beginning_bottom" in tiles[tile_idx]:
            platformImageSurf_beginning_bottom = pygame.image.load("plataformas/img/1_Tiles/" + tiles[tile_idx]["beginning_bottom"]).convert_alpha()
            platformImageSurf_middle_bottom = pygame.image.load("plataformas/img/1_Tiles/" + tiles[tile_idx]["middle_bottom"]).convert_alpha()
            platformImageSurf_end_bottom = pygame.image.load("plataformas/img/1_Tiles/" + tiles[tile_idx]["end_bottom"]).convert_alpha()

        platformImageSurf_unique = pygame.transform.scale(platformImageSurf_unique, (tile_width,tile_height))
        platformImageSurf_beginning = pygame.transform.scale(platformImageSurf_beginning, (tile_width,tile_height))
        platformImageSurf_middle = pygame.transform.scale(platformImageSurf_middle, (tile_width,tile_height))
        platformImageSurf_end = pygame.transform.scale(platformImageSurf_end, (tile_width,tile_height))
        if "beginning_bottom" in tiles[tile_idx]:
            platformImageSurf_beginning_bottom = pygame.transform.scale(platformImageSurf_beginning_bottom, (tile_width,tile_height))
            platformImageSurf_middle_bottom = pygame.transform.scale(platformImageSurf_middle_bottom, (tile_width,tile_height))
            platformImageSurf_end_bottom = pygame.transform.scale(platformImageSurf_end_bottom, (tile_width,tile_height))

        if tileNumber == 1:

            self.surf.blit(platformImageSurf_unique, (0, 0))
        else:

            tileX=0
            idx=0
            while True:
                if idx == 0:

                    self.surf.blit(platformImageSurf_beginning, (tileX, 0))
                elif tileX + tile_width >= width:

                    self.surf.blit(platformImageSurf_end, (tileX, 0))
                else:

                    self.surf.blit(platformImageSurf_middle, (tileX, 0))

                if self.height > tile_height and "beginning_bottom" in tiles[tile_idx]:

                    currentY = tile_height
                    while currentY < self.height:
                        if idx == 0:
                            self.surf.blit(platformImageSurf_beginning_bottom, (tileX, currentY))
                        elif tileX + tile_width >= width:
                            self.surf.blit(platformImageSurf_end_bottom, (tileX, currentY))
                        else:
                            self.surf.blit(platformImageSurf_middle_bottom, (tileX, currentY))
                        currentY += tile_height

                tileX += tile_width
                if tileX > width:
                    break
                idx += 1
        
        self.pos = pygame.math.Vector2(x, alto_ventana-self.height)

        self.rect = self.surf.get_rect(
            topleft=(x, self.pos.y)
        )
        self.speed = .2

        self.surf = self.surf.convert_alpha()

    def update(self, delta_time):
        self.pos.x -= self.speed * globals.game_speed * delta_time
        self.rect.topleft = self.pos