import pygame
import json
from constants import *  # Importa las constantes como el tamaño de la ventana y otras configuraciones
from player import Player  # Importa la clase del jugador
from pygame.locals import *  # Importa los eventos y constantes de pygame
from enemy import Enemy  # Importa la clase del enemigo
from events import *  # Importa eventos personalizados
from fondo import Background  # Importa la clase de fondo
import globals  # Importa la configuración global
import random  # Para generar números aleatorios (por ejemplo, para enemigos)

class Game:
    def __init__(self):
        # Inicializa la pantalla del juego, el reloj y otras variables de estado
        self.screen = pygame.display.set_mode([ancho_ventana, alto_ventana])  # Crear la ventana del juego
        self.clock = pygame.time.Clock()  # Reloj para controlar el frame rate
        self.running = True  # Variable que controla si el juego está en ejecución
        self.started = False  # Variable que indica si el juego ha comenzado

        pygame.init()  # Inicializa todos los módulos de Pygame
        pygame.display.set_caption("Misiles")  # Título de la ventana del juego

        # Fuente para el texto
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.smaller_font = pygame.font.Font('freesansbold.ttf', 22)

        # Cargar el fondo del juego
        self.background = Background()

        self.initialize()  # Llamada para inicializar las variables de inicio del juego

    def initialize(self):
        # Inicializar el tiempo de inicio y la puntuación
        self.start_time = pygame.time.get_ticks()  # Hora actual del inicio del juego
        self.last_frame_time = self.start_time  # Guardar el tiempo del último fotograma
        self.player = Player()  # Crear una instancia del jugador
        self.movement_x = 0  # Dirección horizontal del jugador
        self.movement_y = 0  # Dirección vertical del jugador

        # Temporizador para enemigos (se generan cada 1000 ms)
        self.enemy_timer = 1000
        pygame.time.set_timer(ADD_ENEMY, self.enemy_timer)

        # Grupo de enemigos (usado para manejar las colisiones y el dibujo)
        self.enemies = pygame.sprite.Group()

        # Estado de la partida
        self.lost = False  # Indica si el jugador ha perdido
        self.score = 0  # Puntuación inicial

    def update(self, delta_time):
        # Actualizar el estado del juego en cada frame
        events = pygame.event.get()  # Obtener todos los eventos de Pygame

        for event in events:
            if event.type == pygame.QUIT:  # Si el jugador cierra la ventana
                self.running = False

            elif event.type == KEYDOWN:  # Si una tecla es presionada
                if event.key == K_ESCAPE:  # Si presiona Escape, se cierra el juego
                    self.running = False
                if event.key == K_RETURN and (self.lost or not self.started):  # Comienza el juego si está perdido o aún no iniciado
                    self.started = True
                if event.key == K_r and self.lost:  # Si presiona R, reinicia el juego tras perder
                    self.initialize()
                    self.lost = False  # Restablecer el estado de pérdida

        # Si el jugador ha perdido o el juego no ha comenzado, no actualizar nada más
        if self.lost or not self.started:
            return

        keys = pygame.key.get_pressed()  # Obtener las teclas presionadas
        
        # Movimiento del jugador: controlar con las teclas de dirección o WASD
        if keys[K_LEFT] or keys[K_a]:
            self.movement_x = -1  # Mover a la izquierda
        elif keys[K_RIGHT] or keys[K_d]:
            self.movement_x = 1  # Mover a la derecha
        else:
            self.movement_x = 0  # No moverse en el eje X

        if keys[K_UP] or keys[K_w]:
            self.movement_y = -1  # Mover hacia arriba
        elif keys[K_DOWN] or keys[K_s]:
            self.movement_y = 1  # Mover hacia abajo
        else:
            self.movement_y = 0  # No moverse en el eje Y

        # Incrementar la velocidad del juego con el tiempo (con el tiempo transcurrido desde el inicio)
        globals.game_speed = 1 + ((pygame.time.get_ticks() - self.start_time) / 1000) * 0.1
        self.score = self.score + (delta_time * globals.game_speed)

        # Crear enemigos periódicamente según el temporizador
        for event in events:
            if event.type == ADD_ENEMY:
                num = random.randint(1, 2)  # Número aleatorio de enemigos por cada intervalo
                for e in range(num):
                    enemy = Enemy()  # Crear un nuevo enemigo
                    self.enemies.add(enemy)  # Añadirlo al grupo de enemigos

                # Ajustar el temporizador de generación de enemigos según la velocidad del juego
                self.enemy_timer = 1000 - ((globals.game_speed - 1) * 100)
                if self.enemy_timer < 50:  # No permitir que el temporizador sea menor de 50 ms
                    self.enemy_timer = 50
                pygame.time.set_timer(ADD_ENEMY, int(self.enemy_timer))

        # Actualizar las posiciones del jugador y los enemigos
        self.player.update(self.movement_x, self.movement_y, delta_time)
        self.enemies.update(delta_time)

        # Verificar las colisiones entre el jugador y los enemigos
        self.process_collisions()

        # Actualizar el fondo
        self.background.update(delta_time)

    def process_collisions(self):
        # Verificar si el jugador colide con algún enemigo
        collide = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
        if collide:  # Si hay colisión
            self.lost = True  # El jugador ha perdido
            self.guardar_puntuacion()  # Guardar la puntuación final

    def render(self):
        # Renderizar todos los elementos en pantalla
        self.screen.fill((0, 0, 0))  # Limpiar la pantalla con un fondo negro
        self.background.render(self.screen)  # Dibujar el fondo
        self.screen.blit(self.player.surf, self.player.rect)  # Dibujar al jugador

        # Dibujar todos los enemigos
        for e in self.enemies:
            self.screen.blit(e.surf, e.rect)

        # Mostrar la puntuación
        display_score = round(self.score / 1000)  # Mostrar la puntuación en formato adecuado
        text_score = self.font.render(f'Puntuación: {display_score}', True, (255, 255, 255))  # Texto de puntuación
        scoreTextRect = text_score.get_rect()
        scoreTextRect.top = 5
        scoreTextRect.left = 5
        self.screen.blit(text_score, scoreTextRect)

        # Si el jugador ha perdido
        if self.lost:
            # Mostrar el mensaje de "Game Over"
            game_over_text = self.font.render('¡HAS PERDIDO!', True, (255, 255, 255), (0, 0, 0))
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.center = (ancho_ventana // 2, (alto_ventana // 2) + 200)
            self.screen.blit(game_over_text, game_over_text_rect)

            # Mensaje de reiniciar
            retry_text = self.smaller_font.render('Presiona R para reiniciar', True, (255, 255, 255), (0, 0, 0))
            retry_text_rect = retry_text.get_rect()
            retry_text_rect.center = (ancho_ventana // 2, (alto_ventana // 2) + 225)
            self.screen.blit(retry_text, retry_text_rect)

            # Mostrar las puntuaciones altas
            self.mostrar_puntuaciones_altas()

        # Si el juego no ha comenzado, mostrar el mensaje de inicio
        if not self.started:
            start_text = self.font.render('Presiona Enter para comenzar', True, (255, 255, 255), (0, 0, 0))
            start_text_rect = start_text.get_rect()
            start_text_rect.center = (ancho_ventana // 2, alto_ventana // 2)
            self.screen.blit(start_text, start_text_rect)

        pygame.display.flip()  # Actualizar la pantalla con los nuevos cambios

    def guardar_puntuacion(self):
        # Guardar la puntuación final en un archivo JSON
        puntuacion_final = round(self.score / 1000)
        
        # Intentar cargar las puntuaciones existentes desde el archivo
        try:
            with open('naves/puntuaciones_naves.json', 'r') as file:
                puntuaciones = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            puntuaciones = []

        # Añadir la nueva puntuación a la lista
        puntuaciones.append(puntuacion_final)

        # Ordenar las puntuaciones de mayor a menor
        puntuaciones.sort(reverse=True)

        # Limitar a las 20 mejores puntuaciones
        if len(puntuaciones) > 20:
            puntuaciones = puntuaciones[:20]

        # Guardar las puntuaciones actualizadas en el archivo
        with open('naves/puntuaciones_naves.json', 'w') as file:
            json.dump(puntuaciones, file)

    def mostrar_puntuaciones_altas(self):
        # Mostrar las 5 mejores puntuaciones
        try:
            with open('naves/puntuaciones_naves.json', 'r') as file:
                puntuaciones = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            puntuaciones = []

        y_offset = 130  # La posición inicial para las puntuaciones altas
        for i, puntuacion in enumerate(puntuaciones[:5]):  # Mostrar solo las 5 mejores
            high_score_text = self.font.render(f'{i + 1}. {puntuacion} puntos', True, (255, 255, 255))  # Texto de puntuación
            high_score_rect = high_score_text.get_rect()
            high_score_rect.centerx = ancho_ventana // 2
            high_score_rect.top = y_offset + i * 30
            self.screen.blit(high_score_text, high_score_rect)

    def loop(self):
        # El bucle principal del juego
        while self.running:
            time = pygame.time.get_ticks()
            delta_time = time - self.last_frame_time
            self.last_frame_time = time
            self.update(delta_time)  # Actualizar el estado del juego
            self.render()  # Renderizar la pantalla
            self.clock.tick(60)  # Limitar el juego a 60 fps
        pygame.quit()  # Finalizar Pygame cuando se cierre el juego
