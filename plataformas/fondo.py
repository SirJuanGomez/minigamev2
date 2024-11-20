import pygame
from constants import *  # Asumo que este archivo contiene las variables ancho_ventana y alto_ventana

# Dimensiones de las imágenes del fondo
ASSET_WIDTH = 576
ASSET_HEIGHT = 324

class Background(pygame.sprite.Sprite):
    def __init__(self, add_background, speed, file_num, y_offset):
        super(Background, self).__init__()

        # Inicialización de parámetros
        self.add_background = add_background
        self.speed = speed
        self.y_offset = y_offset
        self.file_num = file_num
        self.base_dir = "plataformas/img/2 Background/fondo/"  # Ruta base de las imágenes

        # Cargar el fondo principal (si está habilitado)
        if self.add_background:
            self.background_surf = self.load_image("1.png")  # Cargar imagen para el fondo principal
            self.background_surf = pygame.transform.scale(self.background_surf, (ancho_ventana, self.background_surf.get_height()))
            self.background_rect = self.background_surf.get_rect()
            self.background_rect.y = alto_ventana - self.background_rect.height

        # Inicializar listas para las imágenes y sus posiciones
        self.surfaces = []
        self.rects = []
        self.positions = []

        # Cargar las imágenes del fondo compuesto (5 imágenes)
        self.load_assets()
        self.setup_assets()

    def load_image(self, path):
        """Carga una imagen desde la ruta proporcionada y la retorna."""
        full_path = self.base_dir + path
        return pygame.image.load(full_path).convert_alpha()

    def load_assets(self):
        """Carga las 5 imágenes que forman el fondo."""
        # Cargar las 5 imágenes del fondo
        for i in range(1, 6):  # Imágenes numeradas 1.png, 2.png, ..., 5.png
            path = f"{i}.png"  # Ruta de cada imagen
            print(f"Loading {path}")  # Solo para depuración
            surf = self.load_image(path)
            surf = pygame.transform.scale(surf, (ASSET_WIDTH, ASSET_HEIGHT))  # Escalar imagen
            self.surfaces.append(surf)
            self.rects.append(surf.get_rect())
            self.positions.append(pygame.math.Vector2(0, 0))  # Posición inicial

    def setup_assets(self):
        """Configura las posiciones de las imágenes cargadas (5 imágenes)."""
        for i, pos in enumerate(self.positions):
            pos.x = ASSET_WIDTH * i  # Posición en el eje X (movimiento horizontal)
            pos.y = alto_ventana - self.rects[i].height + self.y_offset  # Posición en el eje Y (posición vertical)
            self.rects[i].x = pos.x
            self.rects[i].y = pos.y

    def update(self, delta_time):
        """Actualiza la posición de las imágenes para simular el movimiento del fondo."""
        for i, rect in enumerate(self.rects):
            # Mover las imágenes hacia la izquierda con la velocidad asignada
            self.positions[i].x -= self.speed * delta_time
            rect.x = int(self.positions[i].x)
            
            # Si la imagen sale del lado izquierdo de la pantalla, se vuelve a colocar al final
            if rect.x + ASSET_WIDTH <= 0:
                self.positions[i].x = ASSET_WIDTH * len(self.rects)
                rect.x = int(self.positions[i].x)

    def render(self, dest):
        """Dibuja las imágenes del fondo en la pantalla."""
        if self.add_background:
            dest.blit(self.background_surf, self.background_rect)

        # Dibujar todas las superficies del fondo
        for i, surface in enumerate(self.surfaces):
            dest.blit(surface, self.rects[i])
