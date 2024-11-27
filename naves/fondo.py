import pygame
from constants import *  # Importar constantes como el tamaño de la ventana y otras configuraciones

class Background(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializar la clase Background, que es una subclase de pygame.sprite.Sprite
        super(Background, self).__init__()

        # Cargar la imagen de fondo desde el archivo
        self.surf = pygame.image.load('naves/img/nebula.png')
        
        # Calcular el tamaño de la imagen de fondo para que se ajuste al ancho de la ventana
        # El ancho será el doble del ancho de la ventana (ancho_ventana), y la altura se ajustará proporcionalmente
        background_width = ancho_ventana * 2  
        background_height = (background_width / self.surf.get_width()) * self.surf.get_height()
        
        # Redimensionar la imagen de fondo al tamaño calculado
        self.surf = pygame.transform.scale(self.surf, (background_width, background_height))
        
        # Establecer la posición de la primera imagen de fondo, alineada en la parte inferior izquierda de la ventana
        self.rect = self.surf.get_rect(
            bottomleft=(0, alto_ventana)
        )
        
        # Crear una segunda imagen de fondo que se renderizará de la misma manera
        self.surf2 = self.surf
        self.rect2 = self.surf2.get_rect(
            bottomleft=self.rect.topleft  # Colocarla justo encima de la primera imagen de fondo
        )
        
        # Inicializar las posiciones verticales de ambas imágenes de fondo
        self.ypos = 0
        self.ypos2 = background_height - alto_ventana  # La segunda imagen de fondo comienza inmediatamente después de la primera

    def update(self, delta_time):
        # Actualizar la posición vertical de ambas imágenes de fondo para crear un efecto de desplazamiento
        # La velocidad de desplazamiento depende de delta_time (tiempo transcurrido entre fotogramas) para hacer que el movimiento sea independiente de la tasa de fotogramas
        self.ypos += .05 * delta_time
        self.ypos2 += .05 * delta_time
        
        # Actualizar las posiciones de los rectángulos de las imágenes de fondo según sus desplazamientos verticales
        self.rect.y = int(self.ypos)
        self.rect2.y = int(self.ypos2)
        
        # Una vez que la primera imagen de fondo sale de la pantalla, se restablece su posición en la parte superior de la segunda imagen
        if self.rect.y > alto_ventana:
            self.ypos = self.rect2.y - self.surf2.get_height()  # Colocarla justo encima de la segunda imagen de fondo
            self.rect.y = self.ypos
        
        # De manera similar, cuando la segunda imagen de fondo sale de la pantalla, se restablece su posición
        if self.rect2.y > alto_ventana:
            self.ypos2 = self.rect.y - self.surf.get_height()  # Colocarla justo encima de la primera imagen de fondo
            self.rect2.y = self.ypos2

    def render(self, dest):
        # Dibujar ambas imágenes de fondo en la pantalla (dest hace referencia a la superficie donde se renderiza el fondo)
        dest.blit(self.surf, self.rect)   # Renderizar la primera imagen de fondo
        dest.blit(self.surf2, self.rect2)  # Renderizar la segunda imagen de fondo
