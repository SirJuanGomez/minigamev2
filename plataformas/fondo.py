import pygame
from constants import *

class Background(pygame.sprite.Sprite):
    def __init__(self, is_parallax, speed, file_num, y_offset):
        # Inicializa la clase Sprite y establece las variables del fondo
        super(Background, self).__init__()

        self.is_parallax = is_parallax  # Determina si el fondo se mueve con parallax (efecto de desplazamiento a diferentes velocidades)
        self.speed = speed  # La velocidad a la que se mueve el fondo
        self.y_offset = y_offset  # El desplazamiento vertical del fondo
        self.file_num = file_num  # Número del archivo del fondo (aunque no se usa directamente aquí)

        try:
            # Cargar la imagen del fondo desde el archivo especificado
            self.background_surf = pygame.image.load("plataformas/img/2_Background/Background.png").convert_alpha()
            # Escala la imagen para que tenga el mismo ancho que la ventana y ajuste proporcionalmente la altura
            self.background_surf = pygame.transform.scale(self.background_surf, (ancho_ventana, alto_ventana))
            # Obtiene el rectángulo de la imagen para usarlo en la posición y colisiones
            self.background_rect1 = self.background_surf.get_rect()
            self.background_rect2 = self.background_surf.get_rect()
            # Coloca el primer fondo en la posición (0, 0)
            self.background_rect1.x = 0
            self.background_rect1.y = self.y_offset
            # Coloca el segundo fondo justo después del primero, al final de la pantalla
            self.background_rect2.x = ancho_ventana
            self.background_rect2.y = self.y_offset
        except pygame.error as e:
            # Si ocurre un error al cargar la imagen, se captura y se imprime el mensaje de error
            print(f"Error loading background image: {e}")
            self.background_surf = None
            self.background_rect1 = None
            self.background_rect2 = None

    def update(self, delta_time):
        # Actualiza la posición del fondo dependiendo del tiempo transcurrido
        if self.background_surf:
            # Mueve ambos fondos hacia la izquierda según la velocidad y el tiempo transcurrido
            self.background_rect1.x -= self.speed * delta_time
            self.background_rect2.x -= self.speed * delta_time
            
            # Si el primer fondo ha salido completamente de la pantalla por la izquierda,
            # se reposiciona justo después del segundo fondo (efecto de ciclo continuo)
            if self.background_rect1.x <= -self.background_rect1.width:
                self.background_rect1.x = self.background_rect2.x + self.background_rect2.width  # Reposiciona después del segundo fondo

            # Si el segundo fondo ha salido completamente de la pantalla por la izquierda,
            # se reposiciona justo después del primer fondo
            if self.background_rect2.x <= -self.background_rect2.width:
                self.background_rect2.x = self.background_rect1.x + self.background_rect1.width  # Reposiciona después del primer fondo

    def render(self, dest):
        # Renderiza (dibuja) ambos fondos en la pantalla de destino
        if self.background_surf:
            # Dibuja el primer fondo en su posición actual
            dest.blit(self.background_surf, self.background_rect1)
            # Dibuja el segundo fondo en su posición actual
            dest.blit(self.background_surf, self.background_rect2)
