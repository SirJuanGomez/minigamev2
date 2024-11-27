import pygame

# Definición de eventos personalizados usando los identificadores de evento de Pygame

# Evento para crear una nueva plataforma
CREATE_NEW_PLATFORM = pygame.USEREVENT + 1

# Evento para indicar que la boca se ha abierto
MOUTH_OPENED = pygame.USEREVENT + 2

# Evento para indicar que la boca se ha cerrado
MOUTH_CLOSED = pygame.USEREVENT + 3

# Evento para crear una nueva moneda
CREATE_NEW_MONEY = pygame.USEREVENT + 4

# Evento para crear un nuevo enemigo
CREATE_NEW_ENEMY = pygame.USEREVENT + 5

# Evento para crear un nuevo escudo
CREATE_NEW_SHIELD = pygame.USEREVENT + 6
