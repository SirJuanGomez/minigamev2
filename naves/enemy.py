import random  # Importa la librería para generar números aleatorios
import pygame  # Importa Pygame para la creación de juegos
import globals  # Importa el módulo de configuración global
from constants import *  # Importa las constantes definidas, como los tamaños de la ventana

# Tamaño original de la imagen del enemigo (utilizado para el cálculo de escala)
ORIGINAL_SIZE = (512, 512)
# El rango de tamaños para el ancho de los enemigos
MIN_WIDTH = 15
MAX_WIDTH = 80

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializa la clase base Sprite de Pygame
        super(Enemy, self).__init__()

        # Establecer el ancho del enemigo aleatoriamente dentro del rango
        self.width = random.randint(MIN_WIDTH, MAX_WIDTH)
        
        # Calcula la altura proporcionalmente según el tamaño original de la imagen
        self.height = (self.width / ORIGINAL_SIZE[0]) * ORIGINAL_SIZE[1]

        # Cargar la imagen del enemigo desde el archivo y transformarla (convertirla a formato adecuado)
        self.surf = pygame.image.load('naves/img/10.png').convert_alpha()  # Usamos convert_alpha() para manejar transparencia
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))  # Escalar la imagen según el tamaño calculado

        # Crear una máscara de colisión a partir de la imagen del enemigo
        self.mask = pygame.mask.from_surface(self.surf)

        # Establecer el rectángulo de la superficie del enemigo (usado para manejar la posición)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, ancho_ventana),  # Posición aleatoria en el eje X dentro del ancho de la ventana
                random.randint(-100, -20)  # Posición aleatoria en el eje Y fuera de la pantalla (arriba)
            )
        )
        
        # Establecer una velocidad aleatoria para el enemigo, ajustada por la velocidad global del juego
        self.speed = (random.randint(1, 3) / 10) * (1 + ((globals.game_speed) * 3.14 / 5 / 56))

    def update(self, delta_time):
        # Mover al enemigo hacia abajo en la pantalla (dependiendo de su velocidad)
        self.rect.move_ip(0, self.speed * delta_time)
        
        # Actualizar la máscara de colisión en cada fotograma (en caso de que cambie la superficie)
        self.mask = pygame.mask.from_surface(self.surf)
        
        # Si el enemigo sale de la pantalla por la parte inferior, eliminarlo
        if self.rect.top > alto_ventana: 
            self.kill()  # Eliminar el enemigo del grupo de sprites
