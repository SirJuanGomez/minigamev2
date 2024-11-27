import pygame

# Clase que maneja un sprite sheet, que es una imagen que contiene varios fotogramas o sprites.
class SpriteSheet():
    
    # Inicialización de la clase SpriteSheet
    def __init__(self, image):
        # Guardamos la imagen completa del sprite sheet
        self.sheet = image  

    # Método para obtener un fotograma específico del sprite sheet
    def get_image(self, frame, width, height, scale, colour):
        # Creamos una nueva superficie donde vamos a extraer el fotograma
        image = pygame.Surface((width, height)).convert_alpha()  
        
        # Extraemos la sección correspondiente al fotograma del sprite sheet
        # (frame * width) calcula la posición del fotograma en el eje horizontal
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        
        # Redimensionamos la imagen extraída usando el factor de escala
        image = pygame.transform.scale(image, (width * scale, height * scale))
        
        # Establecemos un color como "transparente" en la imagen extraída
        # Cualquier píxel que tenga este color será considerado transparente
        image.set_colorkey(colour)  

        # Devolvemos la imagen del fotograma extraído, ya redimensionado y con la transparencia ajustada
        return image
