import pygame
import sys
import os

# Añadir las carpetas de los juegos a sys.path para importar sus módulos
sys.path.append(os.path.join(os.getcwd(), 'naves'))
sys.path.append(os.path.join(os.getcwd(), 'plataformas'))

# Importar las funciones de game.py desde cada juego
import naves.game  # Juego Naves
import plataformas.game  # Juego Plataformas

# Clase para crear un botón
class Button:
    def __init__(self, text, x, y, width, height, font, color=(255, 255, 255), hover_color=(200, 200, 200)):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)

        # Ajustar el tamaño de la fuente según el tamaño del botón
        self.adjust_font()

    def adjust_font(self):
        """Ajusta el tamaño de la fuente al tamaño del botón."""
        # Calcular el tamaño máximo del texto que cabe en el botón
        max_text_width = self.width * 0.8  # El texto no debe ocupar más del 80% del botón
        max_text_height = self.height * 0.8  # El texto no debe ocupar más del 80% del botón

        # Probar diferentes tamaños de fuente hasta que el texto encaje en el botón
        for size in range(1, 100):
            font = pygame.font.Font(None, size)
            text_surface = font.render(self.text, True, (0, 0, 0))
            if text_surface.get_width() <= max_text_width and text_surface.get_height() <= max_text_height:
                self.font = font  # Establecer la fuente ajustada
            else:
                break  # Detenerse cuando el texto ya no cabe

    def draw(self, screen):
        # Verificar si el mouse está sobre el botón
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, self.hover_color, self.rect)  # Cambiar el color si el mouse está sobre el botón
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # Renderizar el texto del botón
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Verificar si se hizo clic en el botón
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def load_background_images(folder_path):
    """ Cargar todas las imágenes del fondo desde una carpeta y ajustarlas al tamaño de la ventana """
    background_images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (800, 600))  # Ajustar cada imagen al tamaño de la ventana
            background_images.append(image)
    return background_images

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Selecciona un juego")

    # Cargar las imágenes de fondo desde la carpeta
    background_folder = "fondos"  # Asegúrate de que esta carpeta contenga imágenes de fondo
    background_images = load_background_images(background_folder)

    # Intentar cargar una fuente personalizada
    try:
        font_title = pygame.font.Font("PressStart2P.ttf", 72)  # Cambiar el tamaño de la fuente
    except FileNotFoundError:
        font_title = pygame.font.SysFont("Comic Sans MS", 72)  # Fuente alternativa en caso de no encontrar la original

    font = pygame.font.Font(None, 36)

    # Crear botones para los dos juegos, colocados de forma separada
    button_naves = Button("Juego Naves", 150, 250, 200, 50, font)
    button_plataformas = Button("Juego Plataformas", 450, 250, 200, 50, font)

    # Control del fondo desplazable
    fondo_x = 0  # Posición inicial del fondo (horizontal)
    num_images = len(background_images)

    # Velocidad de desplazamiento (más baja para hacer el movimiento más lento)
    move_speed = 0.5  # Menor valor = más lento

    running = True
    while running:
        screen.fill((0, 0, 0))  # Limpiar la pantalla
        
        # Dibujar todas las imágenes del fondo en una secuencia continua
        for i in range(num_images):
            screen.blit(background_images[i], (fondo_x + i * 800, 0))  # Mover cada imagen en la secuencia

        # Desplazar el fondo hacia la izquierda con la velocidad ajustada
        fondo_x -= move_speed
        
        # Reposicionar las imágenes que han salido completamente de la pantalla
        if fondo_x <= -800:
            fondo_x = 0  # Reposicionar al inicio

        # Dibujar el título en la parte superior con borde negro
        title_text = font_title.render("Last Minigame v2", True, (255, 255, 255))  # Blanco
        title_rect = title_text.get_rect(center=(400, 100))  # Centrar en la parte superior pero un poco más abajo

        # Crear un borde negro alrededor del texto
        border_text = font_title.render("Last Minigame v2", True, (0, 0, 0))  # Borde negro
        screen.blit(border_text, title_rect.move(2, 2))  # Desplazar para crear el borde
        screen.blit(title_text, title_rect)  # Dibujar el texto sobre el borde

        # Dibujar los botones
        button_naves.draw(screen)  # Dibujar el botón de Naves
        button_plataformas.draw(screen)  # Dibujar el botón de Plataformas
        pygame.display.flip()  # Actualizar la pantalla de forma continua (sin parpadeo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_naves.is_clicked(event):
                    print("Iniciando Juego Naves...")
                    naves.game.Game().loop()  # Ejecutar Juego Naves
                    running = False
                elif button_plataformas.is_clicked(event):
                    print("Iniciando Juego Plataformas...")
                    plataformas.game.Game().loop()  # Ejecutar Juego Plataformas
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
