import pygame
from pygame.locals import *
import globals
from constants import *
import random

# Definimos el tamaño del sprite del enemigo
ancho=80
alto=80

# Tamaño del asset o recurso gráfico (en este caso, el tamaño de cada cuadro de animación)
asset_size=32

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializa el sprite del enemigo, heredando de pygame.sprite.Sprite
        super(Enemy, self).__init__()
        
        # El nombre de la animación actual del enemigo
        self.current_animation = "walk"
        
        # Diccionario para almacenar las animaciones
        self.animations = {}
        
        # Comportamiento de las animaciones (en este caso, "walk" es continua)
        self.animation_behaviour = {
            "walk": "continuous"
        }

        # Carga los assets o recursos gráficos para las animaciones
        self.load_assets()

        # Índice para la animación, velocidad de la animación, y superficie (imagen) del sprite
        self.idxAnimation = 0
        self.animationSpeed = .15
        self.surf = self.animations[self.current_animation][self.idxAnimation]
        self.surf = pygame.transform.scale(self.surf, (ancho,alto))  # Escala el sprite a las dimensiones definidas
        self.rect = self.surf.get_rect()  # Rectángulo que define la posición del sprite
        self.pos = pygame.math.Vector2(
            ancho_ventana, 
            random.randrange(int(alto_ventana*.5), int(alto_ventana*.8))
        )  # Posición inicial del enemigo, en un rango vertical aleatorio
        self.speed = random.randrange (2,4) / 10  # Velocidad aleatoria para el enemigo
        self.update_mask()  # Actualiza la máscara para la colisión

    def load_assets(self):
        # Carga los frames de la animación "walk"
        self.animations["walk"] = []
        asset = pygame.image.load("plataformas/img/7 Bird/Walk.png").convert_alpha()  # Carga la imagen de la animación
        asset = pygame.transform.flip(asset,flip_x=90,flip_y=0)  # Voltea la imagen en el eje X
        width = asset.get_width()  # Obtiene el ancho de la imagen
        idx = 0
        # Divide la imagen en varios cuadros según el tamaño del asset
        while (idx*asset_size < width):
            frame = pygame.Surface((asset_size, asset_size), pygame.SRCALPHA)  # Crea un nuevo "frame" para la animación
            frame.blit(asset, asset.get_rect(), Rect(idx*asset_size, 0, asset_size, asset_size))  # Recorta el cuadro de la imagen
            self.animations["walk"].append(
                frame.convert_alpha()  # Añade el cuadro a la lista de animación
            )
            idx+=1  # Incrementa el índice para el siguiente cuadro

    def animate(self, delta_time):
        # Actualiza la animación según el tiempo que ha pasado
        self.animationSpeed = .008 * delta_time
        self.idxAnimation += self.animationSpeed  # Incrementa el índice de la animación basado en la velocidad
        # Si la animación ha terminado, reinicia si es continua
        if int(self.idxAnimation)+1 >= len(self.animations[self.current_animation]):
            if self.animation_behaviour[self.current_animation] == "continuous":
                self.idxAnimation = 0  # Reinicia la animación
            else:
                self.idxAnimation = len(self.animations[self.current_animation])-1  # Si no es continua, detiene la animación en el último cuadro
        # Actualiza la superficie con el siguiente cuadro de animación
        self.surf = self.animations[self.current_animation][int(self.idxAnimation)]
        self.surf = pygame.transform.scale(self.surf, (ancho,alto))  # Escala el sprite
        self.surf= pygame.transform.rotate(self.surf,15)  # Rota ligeramente el sprite
        self.rect = self.surf.get_rect()  # Actualiza el rectángulo de colisión

    def update(self, delta_time):
        # Actualiza la posición y animación del enemigo
        self.animate(delta_time)
        self.pos.x -= self.speed * globals.game_speed * delta_time  # Mueve el enemigo hacia la izquierda
        self.rect.x = int(self.pos.x)  # Actualiza la posición horizontal en el rectángulo
        self.rect.y = int(self.pos.y)  # Actualiza la posición vertical en el rectángulo

        # Si el enemigo sale de la pantalla por la izquierda, se elimina
        if (self.rect.x + ancho) < 0:
            self.kill()  # Elimina el sprite
        self.update_mask()  # Actualiza la máscara de colisión

    def update_mask(self):
        # Actualiza la máscara para la detección de colisiones
        self.maskSurface = self.surf
        self.maskSurface = pygame.transform.scale(self.maskSurface, (ancho*.9,alto*.9))  # Escala la superficie de la máscara
        self.mask = pygame.mask.from_surface(self.maskSurface)  # Crea la máscara a partir de la superficie
