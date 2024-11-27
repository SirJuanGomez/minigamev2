import pygame
from pygame.locals import *
import globals
from constants import *
import random

# Dimensiones del objeto "dinero" (tarjeta)
WIDTH = 48
HEIGHT = 48

ASSET_SIZE = 24  # Tamaño de cada cuadro en la animación

class Money(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializa la clase Sprite de Pygame
        super(Money, self).__init__()

        self.current_animation = "idle"  # La animación actual es "idle" (inactiva)
        self.animations = {}  # Un diccionario para almacenar las animaciones
        self.animation_behaviour = {
            "idle": "continuous"  # La animación "idle" se repite de forma continua
        }

        self.load_assets()  # Carga los activos (imágenes)

        self.idxAnimation = 0  # Índice de la animación actual
        self.animationSpeed = .15  # Velocidad de la animación
        self.surf = self.animations[self.current_animation][self.idxAnimation]  # Obtiene el cuadro de la animación
        self.surf = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))  # Escala la superficie del sprite
        self.rect = self.surf.get_rect()  # Obtiene el rectángulo del sprite para manejar la posición
        self.pos = pygame.math.Vector2(
            ancho_ventana,  # Posición inicial en el eje X (fuera de la pantalla a la derecha)
            random.randrange(int(alto_ventana * .5), int(alto_ventana * .8))  # Posición aleatoria en el eje Y
        )
        self.speed = random.randrange(2, 4) / 10  # Velocidad de movimiento aleatoria del objeto

    def load_assets(self):
        # Carga los activos (imágenes) para la animación
        self.animations["idle"] = []  # Lista para la animación "idle"
        # Carga la imagen de la tarjeta que se usará como sprite
        asset = pygame.image.load("plataformas/img/4 Animated objects/Card.png").convert_alpha()
        width = asset.get_width()  # Obtiene el ancho de la imagen cargada
        idx = 0
        while (idx * ASSET_SIZE < width):  # Extrae cada cuadro de la imagen
            # Crea una nueva superficie para un cuadro de la animación
            frame = pygame.Surface((ASSET_SIZE, ASSET_SIZE), pygame.SRCALPHA)
            # Recorta un cuadro de la imagen original y lo copia en la nueva superficie
            frame.blit(asset, asset.get_rect(), Rect(idx * ASSET_SIZE, 0, ASSET_SIZE, ASSET_SIZE))
            # Agrega el cuadro de animación a la lista
            self.animations["idle"].append(
                frame.convert_alpha()
            )
            idx += 1  # Incrementa el índice para cargar el siguiente cuadro

    def animate(self, delta_time):
        # Actualiza la animación según el tiempo transcurrido
        self.animationSpeed = .008 * delta_time  # Calcula la velocidad de la animación en función del delta_time
        self.idxAnimation += self.animationSpeed  # Avanza en el índice de la animación
        # Si hemos llegado al final de la animación, reinicia o detén el ciclo dependiendo del comportamiento
        if int(self.idxAnimation) + 1 >= len(self.animations[self.current_animation]):
            if self.animation_behaviour[self.current_animation] == "continuous":
                self.idxAnimation = 0  # Reinicia la animación si es continua
            else:
                self.idxAnimation = len(self.animations[self.current_animation]) - 1  # Se detiene en el último cuadro
        # Obtiene el cuadro actual de la animación y lo escala
        self.surf = self.animations[self.current_animation][int(self.idxAnimation)]
        self.surf = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))
        self.rect = self.surf.get_rect()  # Actualiza el rectángulo del sprite

    def update(self, delta_time):
        # Actualiza la posición del objeto y la animación
        self.animate(delta_time)  # Llama a la función para actualizar la animación
        self.pos.x -= self.speed * globals.game_speed * delta_time  # Mueve el objeto a la izquierda
        self.rect.x = int(self.pos.x)  # Actualiza la posición del rectángulo en el eje X
        self.rect.y = int(self.pos.y)  # Actualiza la posición del rectángulo en el eje Y

        # Si el objeto se ha movido fuera de la pantalla, lo elimina
        if (self.rect.x + WIDTH) < 0:
            self.kill()

    # Llamar para mostrar el hitbox del sprite (solo para fines de depuración)
    def display_hitbox(self, dest):
        # Crea una superficie semi-transparente que representa el hitbox
        debugRect = pygame.Surface((self.rect.width, self.rect.height))
        debugRect.set_alpha(128)  # Establece la transparencia (0-255, 128 es semi-transparente)
        debugRect.fill((0, 255, 0))  # Colorea el hitbox de verde
        pygame.display.get_surface().blit(debugRect, (self.rect.x, self.rect.y))  # Dibuja el hitbox en la pantalla
