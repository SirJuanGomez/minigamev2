import pygame
def calcular_tamano_fotograma(hoja_sprites):
    # Obtener el tamaño de la imagen de la hoja de sprites
    ancho_hoja, alto_hoja = hoja_sprites.get_size()

    # Calcular el número de fotogramas en la hoja (suponiendo que están dispuestos horizontalmente o verticalmente)
    # Esto depende de cómo estén organizados los fotogramas. Aquí te muestro dos casos:

    # Caso 1: Fotogramas dispuestos horizontalmente
    num_fotogramas_horizontales = ancho_hoja // alto_hoja  # Asumimos que el ancho de cada fotograma es igual a su alto
    fotograma_width = ancho_hoja // num_fotogramas_horizontales
    fotograma_height = alto_hoja

    # Caso 2: Fotogramas dispuestos verticalmente
    num_fotogramas_verticales = alto_hoja // alto_hoja  # Asumimos que la altura de cada fotograma es igual
    fotograma_width = ancho_hoja
    fotograma_height = alto_hoja // num_fotogramas_verticales

    # Puedes calcular ambos casos si los fotogramas están dispuestos tanto horizontal como verticalmente
    return fotograma_width, fotograma_height

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
ancho_ventana = 800
alto_ventana = 600

# Crear la ventana
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))

# Cargar la hoja de sprites
hoja_sprites = pygame.image.load("plataformas/img/7 Bird/Walk.png").convert_alpha()

# Calcular el tamaño de cada fotograma
fotograma_width, fotograma_height = calcular_tamano_fotograma(hoja_sprites)

# Mostrar el tamaño de cada fotograma
print(f"El tamaño de cada fotograma es: {fotograma_width}x{fotograma_height}")

# Bucle principal del juego (por ejemplo)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar la pantalla (con un color, por ejemplo)
    pantalla.fill((0, 0, 0))  # Rellenar la pantalla con color negro

    # Actualizar la pantalla
    pygame.display.flip()

# Cerrar Pygame
pygame.quit()
