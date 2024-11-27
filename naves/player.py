import pygame
from constants import *

# Definición de tamaño original de la imagen del jugador y el tamaño final que tendrá
orig_size = (196, 196)  # Tamaño original de la imagen del jugador
ancho = 90  # Ancho del jugador ajustado
alto = (ancho / orig_size[0]) * orig_size[1]  # Altura proporcionalmente ajustada
speed = 0.25  # Velocidad de movimiento del jugador

class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializa la clase base Sprite de Pygame
        super(Player, self).__init__()

        # Carga la imagen del jugador y la transforma a un tamaño ajustado
        self.surf = pygame.image.load("naves/img/Idle.png").convert_alpha()  # Cargar imagen con transparencia
        self.surf = pygame.transform.scale(self.surf, (ancho, alto))  # Escalar imagen al tamaño deseado
        self.update_mask()  # Actualizar la máscara de colisión

        # Guardar la imagen original para poder rotarla sin perder la imagen original
        self.original_surf = self.surf
        self.lastRotation = 0  # Inicializa la rotación en 0 grados

        # Definir el rectángulo del jugador, centrado en la parte inferior de la ventana
        self.rect = self.surf.get_rect(
            center=(
                (ancho_ventana / 2) - (ancho / 2),  # Centrado en el eje X
                (alto_ventana - alto)  # En el borde inferior de la ventana
            )
        )

    def update(self, movement_x, movement_y, delta_time):
        # Mover al jugador según las teclas presionadas, con un ajuste por la velocidad y el tiempo
        self.rect.move_ip(speed * movement_x * delta_time, speed * movement_y * delta_time)

        # Calcular la rotación del jugador dependiendo de la dirección del movimiento en el eje X
        rotation = 45 * movement_x * -1  # Rotación de 45 grados por unidad en el eje X
        self.surf = pygame.transform.rotate(self.original_surf, self.lerp(self.lastRotation, rotation, .25))
        self.lastRotation = rotation  # Actualizar la última rotación
        self.update_mask()  # Actualizar la máscara de colisión

        # Rotar la imagen por 90 grados antes de dibujarla
        self.surf = pygame.transform.rotate(self.surf, 90)  # Rotar la imagen final 90 grados

        # Ajustar el rectángulo para asegurarse de que el sprite se mantenga centrado después de la rotación
        self.rect = self.surf.get_rect(center=self.rect.center)

        # Limitar el movimiento del jugador a los bordes de la ventana
        if self.rect.left < 0: self.rect.left = 0  # No puede ir más allá del borde izquierdo
        if self.rect.right > ancho_ventana: self.rect.right = (ancho_ventana - 2)  # No puede ir más allá del borde derecho
        if self.rect.top <= 0: self.rect.top = 0  # No puede salir de la parte superior
        if self.rect.bottom >= alto_ventana: self.rect.bottom = (alto_ventana - 50)  # No puede salir de la parte inferior

    def lerp(self, a: float, b: float, t: float) -> float:
        # Función de interpolación lineal para suavizar la rotación
        return (1 - t) * a + t * b  # Interpola entre dos valores a y b con el factor t

    def update_mask(self):
        # Crea una máscara de colisión más pequeña para 'perdonar' las colisiones con el jugador
        maskSurface = self.surf
        maskSurface = pygame.transform.scale(maskSurface, (ancho * .7, alto * .8))  # Reducir la imagen para la máscara
        self.mask = pygame.mask.from_surface(maskSurface)  # Crear la máscara de colisión a partir de la superficie escalada
