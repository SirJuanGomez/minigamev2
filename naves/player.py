import pygame
from constants import *

orig_size = (196, 196)
ancho = 90
alto = (ancho / orig_size[0]) * orig_size[1]
speed = 0.25

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.image.load("naves/img/Idle.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (ancho, alto))
        self.update_mask()

        # Guardar para manejar bien las rotaciones
        self.original_surf = self.surf
        self.lastRotation = 0

        self.rect = self.surf.get_rect(
            center=(
                (ancho_ventana / 2) - (ancho / 2),
                (alto_ventana - alto)
            )
        )

    def update(self, movement_x, movement_y, delta_time):
        self.rect.move_ip(speed * movement_x * delta_time, speed * movement_y * delta_time)

        rotation = 45 * movement_x * -1
        self.surf = pygame.transform.rotate(self.original_surf, self.lerp(self.lastRotation, rotation, .25))
        self.lastRotation = rotation
        self.update_mask()

        # Rotate by 90 degrees before drawing
        self.surf = pygame.transform.rotate(self.surf, 90)  # Rotate by 90 degrees

        # Adjust the rect to ensure the sprite remains centered after rotation
        self.rect = self.surf.get_rect(center=self.rect.center)

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > ancho_ventana: self.rect.right = (ancho_ventana - 2)
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= alto_ventana: self.rect.bottom = (alto_ventana - 50)

    def lerp(self, a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b

    def update_mask(self):
        # Mascara tiene un 90% del tamaño para 'perdonar' al jugador en ciertas colisiones
        maskSurface = self.surf
        maskSurface = pygame.transform.scale(maskSurface, (ancho * .7, alto * .8))
        self.mask = pygame.mask.from_surface(maskSurface)
