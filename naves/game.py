import pygame
import json
from constants import *
from player import Player
from pygame.locals import *
from enemy import Enemy
from events import *
from fondo import Background
import globals
import random


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([ancho_ventana, alto_ventana])
        self.clock = pygame.time.Clock()
        self.running = True
        self.started = False

        pygame.init()
        pygame.display.set_caption("Misiles")

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.smaller_font = pygame.font.Font('freesansbold.ttf', 22)
        self.background = Background()

        self.initialize()

    def initialize(self):
        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = self.start_time
        self.player = Player()
        self.movement_x = 0
        self.movement_y = 0

        #Timers
        self.enemy_timer = 1000
        pygame.time.set_timer(ADD_ENEMY, self.enemy_timer)

        self.enemies = pygame.sprite.Group()

        self.lost = False
        self.score = 0

    def update(self, delta_time):
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_RETURN and (self.lost or not self.started):
                        self.started = True
                    if event.key == K_r and self.lost:  # Comprobar si se presiona 'R' para reiniciar
                        self.initialize()
                        self.lost = False  # Reiniciar el estado de pérdida

            if self.lost or not self.started:
                return

            keys = pygame.key.get_pressed()  
            

            if keys[K_LEFT] or keys[K_a]:
                self.movement_x = -1  
            elif keys[K_RIGHT] or keys[K_d]:
                self.movement_x = 1  
            else:
                self.movement_x = 0  


            if keys[K_UP] or keys[K_w]:
                self.movement_y = -1  
            elif keys[K_DOWN] or keys[K_s]:
                self.movement_y = 1  
            else:
                self.movement_y = 0  

            globals.game_speed = 1 + ((pygame.time.get_ticks() - self.start_time) / 1000) * 0.1
            self.score = self.score + (delta_time * globals.game_speed)

            for event in events:
                if event.type == ADD_ENEMY:
                    num = random.randint(1, 2)
                    for e in range(num):
                        enemy = Enemy()
                        self.enemies.add(enemy)

                    self.enemy_timer = 1000 - ((globals.game_speed - 1) * 100)
                    if self.enemy_timer < 50: 
                        self.enemy_timer = 50
                    pygame.time.set_timer(ADD_ENEMY, int(self.enemy_timer))


            self.player.update(self.movement_x, self.movement_y, delta_time)
            self.enemies.update(delta_time)
            self.process_collisions()
            self.background.update(delta_time)
            
    def process_collisions(self):
        collide = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
        if collide:
            self.lost = True
            self.guardar_puntuacion()

    def render(self):
        self.screen.fill((0, 0, 0))  # Fondo negro
        self.background.render(self.screen)
        self.screen.blit(self.player.surf, self.player.rect)

        for e in self.enemies:
            self.screen.blit(e.surf, e.rect)

        # Mostrar puntuación actual del jugador
        display_score = round(self.score / 1000)
        text_score = self.font.render(f'Puntuación: {display_score}', True, (255, 255, 255))  # Sin "puntos"
        scoreTextRect = text_score.get_rect()
        scoreTextRect.top = 5
        scoreTextRect.left = 5
        self.screen.blit(text_score, scoreTextRect)

        if self.lost:
            # Mensaje de "Game Over"
            game_over_text = self.font.render('¡HAS PERDIDO!', True, (255, 255, 255), (0, 0, 0))
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.center = (ancho_ventana // 2, (alto_ventana // 2)+200)
            self.screen.blit(game_over_text, game_over_text_rect)

            # Mensaje de reiniciar
            retry_text = self.smaller_font.render('Presiona R para reiniciar', True, (255, 255, 255), (0, 0, 0))
            retry_text_rect = retry_text.get_rect()
            retry_text_rect.center = (ancho_ventana // 2, (alto_ventana // 2) + 225)
            self.screen.blit(retry_text, retry_text_rect)

            # Mostrar las puntuaciones altas centradas
            self.mostrar_puntuaciones_altas()

        if not self.started:
            # Mensaje para iniciar el juego
            start_text = self.font.render('Presiona Enter para comenzar', True, (255, 255, 255), (0, 0, 0))
            start_text_rect = start_text.get_rect()
            start_text_rect.center = (ancho_ventana // 2, alto_ventana // 2)
            self.screen.blit(start_text, start_text_rect)

        pygame.display.flip()

    def guardar_puntuacion(self):
        # Obtener la puntuación final
        puntuacion_final = round(self.score / 1000)
        
        # Intentar cargar el archivo JSON existente (si existe)
        try:
            with open('naves/puntuaciones_naves.json', 'r') as file:
                puntuaciones = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            puntuaciones = []
        
        # Agregar la nueva puntuación a la lista
        puntuaciones.append(puntuacion_final)

        # Ordenar las puntuaciones de mayor a menor
        puntuaciones.sort(reverse=True)

        # Asegurarse de que haya un máximo de 20 puntuaciones
        if len(puntuaciones) > 20:
            puntuaciones = puntuaciones[:20]

        # Guardar las puntuaciones en el archivo
        with open('naves/puntuaciones_naves.json', 'w') as file:
            json.dump(puntuaciones, file)
            
    def mostrar_puntuaciones_altas(self):
    # Intentamos cargar las puntuaciones
        try:
            with open('naves/puntuaciones_naves.json', 'r') as file:
                puntuaciones = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            puntuaciones = []

        # Mostrar las 5 primeras puntuaciones
        y_offset = 130  # Empieza un poco más abajo de la parte inferior de la pantalla
        for i, puntuacion in enumerate(puntuaciones[:5]):  # Mostramos solo las 5 mejores
            high_score_text = self.font.render(f'{i + 1}. {puntuacion} puntos', True, (255, 255, 255))  # Aquí agregamos "puntos"
            high_score_rect = high_score_text.get_rect()
            high_score_rect.centerx = ancho_ventana // 2
            high_score_rect.top = y_offset + i * 30
            self.screen.blit(high_score_text, high_score_rect)

    def loop(self):
        while self.running:
            time = pygame.time.get_ticks()
            delta_time = time - self.last_frame_time
            self.last_frame_time = time
            self.update(delta_time)
            self.render()
            self.clock.tick(60)
        pygame.quit()

