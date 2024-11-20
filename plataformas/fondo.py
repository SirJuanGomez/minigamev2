import pygame
from constants import *

class Background(pygame.sprite.Sprite):
    def __init__(self, is_parallax, speed, file_num, y_offset):
        super(Background, self).__init__()

        self.is_parallax = is_parallax  # Determina si se mueve con parallax
        self.speed = speed
        self.y_offset = y_offset
        self.file_num = file_num

        try:
            # Cargar la imagen del fondo
            self.background_surf = pygame.image.load("plataformas/img/2_Background/Background.png").convert_alpha()
            # Escalar la imagen para que tenga el ancho de la pantalla (ancho_ventana) y se ajuste proporcionalmente en altura
            self.background_surf = pygame.transform.scale(self.background_surf, (ancho_ventana, alto_ventana))
            self.background_rect1 = self.background_surf.get_rect()
            self.background_rect2 = self.background_surf.get_rect()
            # Colocar el primer fondo en la posición (0, 0)
            self.background_rect1.x = 0
            self.background_rect1.y = self.y_offset
            # Colocar el segundo fondo inmediatamente después del primero
            self.background_rect2.x = ancho_ventana
            self.background_rect2.y = self.y_offset
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background_surf = None
            self.background_rect1 = None
            self.background_rect2 = None

    def update(self, delta_time):
        if self.background_surf:
            # Mover el primer fondo hacia la izquierda
            self.background_rect1.x -= self.speed * delta_time
            # Mover el segundo fondo hacia la izquierda
            self.background_rect2.x -= self.speed * delta_time
            
            # Si el primer fondo ha salido completamente de la pantalla (a la izquierda), lo reposicionamos al final del segundo fondo
            if self.background_rect1.x <= -self.background_rect1.width:
                self.background_rect1.x = self.background_rect2.x + self.background_rect2.width  # Reposiciona después del segundo fondo

            # Si el segundo fondo ha salido completamente de la pantalla (a la izquierda), lo reposicionamos al final del primer fondo
            if self.background_rect2.x <= -self.background_rect2.width:
                self.background_rect2.x = self.background_rect1.x + self.background_rect1.width  # Reposiciona después del primer fondo

    def render(self, dest):
        if self.background_surf:
            dest.blit(self.background_surf, self.background_rect1)
            dest.blit(self.background_surf, self.background_rect2)
