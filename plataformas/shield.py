import pygame
from pygame.locals import *
import globals
from constants import *
import random

WIDTH = 48  # Ancho del escudo
HEIGHT = 48  # Alto del escudo

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializa la clase Sprite, que es la clase base de Pygame para todos los objetos visuales
        super(Shield, self).__init__()

        # Cargar la imagen del escudo desde un archivo
        self.surf = pygame.image.load("plataformas/img/shield-small.png")

        # Obtener el rectángulo de la imagen (necesario para manipular la posición en pantalla)
        self.rect = self.surf.get_rect()

        # Asignar una posición aleatoria para el escudo (en la parte derecha de la pantalla, a medio camino verticalmente)
        self.pos = pygame.math.Vector2(
            ancho_ventana,  # La posición inicial en el eje X será al final de la pantalla (derecha)
            random.randrange(int(ancho_ventana * 0.5), int(alto_ventana * 0.8))  # Y será aleatorio entre la mitad y el 80% de la altura de la pantalla
        )

        # La velocidad de movimiento del escudo es aleatoria, entre 0.2 y 0.4
        self.speed = random.randrange(2, 4) / 10

    def update(self, delta_time):
        # Actualiza la posición del escudo, moviéndolo hacia la izquierda (hacia el jugador)
        self.pos.x -= self.speed * globals.game_speed * delta_time  # Movimiento hacia la izquierda

        # Actualizar las coordenadas del rectángulo (posición del escudo)
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

        # Si el escudo ha salido de la pantalla por la izquierda, lo eliminamos
        if (self.rect.x + WIDTH) < 0:
            self.kill()

    def display_hitbox(self, dest):
        # Muestra el hitbox del escudo, útil para depuración
        debugRect = pygame.Surface((self.rect.width, self.rect.height))  # Crear una superficie con las dimensiones del rectángulo
        debugRect.set_alpha(128)  # Establece la transparencia
        debugRect.fill((0, 255, 0))  # Colorea el rectángulo de color verde

        # Dibuja el hitbox en la pantalla de Pygame
        pygame.display.get_surface().blit(debugRect, (self.rect.x, self.rect.y))
